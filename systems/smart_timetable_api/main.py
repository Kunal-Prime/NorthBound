# main.py

import os
import time
import logging
from datetime import datetime


from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import google.generativeai as genai

from sqlalchemy.orm import Session
from models import Base, Timetable, SessionLocal, engine

from systems.smart_timetable_api.parsers import manual_parser, llm_parser
from systems.smart_timetable_api.evaluator import evaluate

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Configuration - Be explicit, not lazy
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://your-railway-url.railway.app",
        "https://api.yourdomain.xyz",           # your custom domain
        "https://yourusername.github.io"        # GitHub Pages
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rest of your code...
# ── APP (MUST BE FIRST BEFORE ANY DECORATOR USE) ──────────
app = FastAPI(
    title="Smart Timetable Parser API",
    description="Hybrid system using rule-based + LLM parsing with decision logic",
    version="2.0"
)

# ── DB SESSION ────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── STARTUP (NOW SAFE) ────────────────────────────────────
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# ── ENV ───────────────────────────────────────────────────
load_dotenv()

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
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
    return {"message": "Smart Timetable Parser API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

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
def compare(request: Request, data: TimetableInput):

    manual_result = None
    llm_result = None

    try:
        manual_result = manual_parser.parse(data.text)
    except:
        pass

    try:
        llm_result = llm_parser.parse(data.text)
    except:
        pass

    decision = evaluate(manual_result, llm_result)

    return {
        "manual": manual_result,
        "llm": llm_result,
        "decision": decision
    }


# ── SMART PARSE ───────────────────────────────────────────
@app.post("/smart-parse")
def smart_parse(request: Request, data: TimetableInput):

    try:
        manual_result = manual_parser.parse(data.text)
    except:
        manual_result = None

    try:
        llm_result = llm_parser.parse(data.text)
    except:
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