import os
import time
import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import google.generativeai as genai

from sqlalchemy import text
from sqlalchemy.orm import Session
from models import Base, Timetable, SessionLocal, engine

from systems.smart_timetable_api.parsers import manual_parser, llm_parser
from systems.smart_timetable_api.evaluator import evaluate


# ── ENV ───────────────────────────────────────────────────
load_dotenv()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
APP_ENV = os.getenv("APP_ENV", "production")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

genai.configure(api_key=api_key)


# ── LOGGING ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── RATE LIMITER ──────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


# ── APP (CREATE ONLY ONCE) ────────────────────────────────
app = FastAPI(
    title="Smart Timetable Parser API",
    description="Hybrid system using rule-based + LLM parsing with decision logic",
    version="2.0",
    debug=DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://kunal-prime.github.io",
        "https://northbound-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ── DB SESSION ────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── STARTUP ───────────────────────────────────────────────
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    logger.info(f"App started | env={APP_ENV} | debug={DEBUG}")


# ── MODELS ────────────────────────────────────────────────
class TimetableInput(BaseModel):
    text: str

    @validator("text")
    def validate_text(cls, value):
        if not value.strip():
            raise ValueError("text cannot be empty")
        if len(value) > 5000:
            raise ValueError("text too long")
        return value


class TimetableCreate(BaseModel):
    title: str
    data: str


# ── ROOT ──────────────────────────────────────────────────
@app.get("/")
def home():
    return {
        "message": "Smart Timetable Parser API",
        "version": "2.0",
        "env": APP_ENV,
        "endpoints": {
            "POST /parse-manual": "Rule-based parser",
            "POST /parse-llm": "AI-powered parser",
            "POST /compare": "Run both and compare",
            "POST /smart-parse": "Primary frontend endpoint",
            "POST /parse-and-save": "Save parsed timetable",
            "GET /timetables": "List saved timetables",
            "GET /health": "System status"
        }
    }


@app.get("/health")
def health_check():
    health = {
        "status": "ok",
        "env": APP_ENV,
        "debug": DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }

    health["checks"]["app"] = "ok"

    # API key
    if api_key:
        health["checks"]["api_key"] = "present"
    else:
        health["checks"]["api_key"] = "missing"
        health["status"] = "degraded"

    # Database
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health["checks"]["database"] = "reachable"
    except Exception as e:
        health["checks"]["database"] = "unreachable"
        health["status"] = "degraded"
        logger.error(f"Health check DB failed: {e}")

    # LLM
    try:
        test_model = genai.GenerativeModel("gemini-1.5-flash")
        test_response = test_model.generate_content("Reply with: ok")
        if test_response.text:
            health["checks"]["llm"] = "reachable"
    except Exception as e:
        health["checks"]["llm"] = "unreachable"
        health["status"] = "degraded"
        logger.error(f"Health check LLM failed: {e}")

    return health


# ── MANUAL PARSER ─────────────────────────────────────────
@app.post("/parse-manual")
@limiter.limit("30/minute")
def parse_manual(request: Request, data: TimetableInput):
    logger.info(f"manual | {len(data.text)} chars")

    try:
        result = manual_parser.parse(data.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"parser": "manual", "result": result}


# ── LLM PARSER ────────────────────────────────────────────
@app.post("/parse-llm")
@limiter.limit("5/minute")
def parse_llm(request: Request, data: TimetableInput):
    logger.info(f"llm | {len(data.text)} chars")

    try:
        result = llm_parser.parse(data.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"parser": "llm", "result": result}


# ── COMPARE ───────────────────────────────────────────────
@app.post("/compare")
@limiter.limit("5/minute")
def compare(request: Request, data: TimetableInput):
    manual_result = None
    llm_result = None

    try:
        manual_result = manual_parser.parse(data.text)
    except Exception:
        pass

    try:
        llm_result = llm_parser.parse(data.text)
    except Exception:
        pass

    decision = evaluate(manual_result, llm_result)

    return {
        "manual": manual_result,
        "llm": llm_result,
        "decision": decision
    }


# ── SMART PARSE ───────────────────────────────────────────
@app.post("/smart-parse")
@limiter.limit("10/minute")
def smart_parse(request: Request, data: TimetableInput):
    try:
        manual_result = manual_parser.parse(data.text)
    except Exception:
        manual_result = None

    try:
        llm_result = llm_parser.parse(data.text)
    except Exception:
        llm_result = None

    decision = evaluate(manual_result, llm_result)

    return {
        "decision": decision,
        "manual": manual_result,
        "llm": llm_result
    }


# ── DB ENDPOINTS ──────────────────────────────────────────
@app.post("/parse-and-save")
def parse_and_save(timetable: TimetableCreate, db: Session = Depends(get_db)):
    db_timetable = Timetable(
        title=timetable.title,
        data=timetable.data
    )

    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)

    return {"id": db_timetable.id, "message": "saved"}


@app.get("/timetables")
def list_timetables(db: Session = Depends(get_db)):
    return db.query(Timetable).all()


@app.get("/timetables/{timetable_id}")
def get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    item = db.query(Timetable).filter(Timetable.id == timetable_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="not found")

    return item 