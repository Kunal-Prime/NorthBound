# main.py

import os
import time
import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import google.generativeai as genai

# Clean imports
from systems.smart_timetable_api.parsers import manual_parser, llm_parser
from systems.smart_timetable_api.evaluator import evaluate

load_dotenv()

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# ── Rate Limiter ──────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ── App ───────────────────────────────────────────────────
app = FastAPI(
    title="Smart Timetable Parser API",
    description="Hybrid system using rule-based + LLM parsing with decision logic",
    version="2.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Models ────────────────────────────────────────────────
class TimetableInput(BaseModel):
    text: str

    @validator("text")
    def text_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("text cannot be empty")
        if len(value) > 5000:
            raise ValueError("text is too long (max 5000 characters)")
        return value

# ── Routes ────────────────────────────────────────────────

@app.get("/")
def home():
    return {
        "message": "Smart Timetable Parser API",
        "version": "2.0",
        "endpoints": {
            "POST /parse-manual": "Rule-based parser",
            "POST /parse-llm": "AI-powered parser",
            "POST /compare": "Compare both outputs",
            "POST /smart-parse": "Auto-select best parser (🔥)",
            "GET /health": "System status"
        }
    }


@app.get("/health")
def health_check():
    health = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }

    health["checks"]["app"] = "ok"

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        health["checks"]["api_key"] = "present"
    else:
        health["checks"]["api_key"] = "missing"
        health["status"] = "degraded"

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


# ── Manual Parser ─────────────────────────────────────────

@app.post("/parse-manual")
@limiter.limit("30/minute")
def parse_manual(request: Request, data: TimetableInput):

    logger.info(f"POST /parse-manual | length={len(data.text)}")
    start = time.time()

    try:
        result = manual_parser.parse(data.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    duration = round(time.time() - start, 3)

    return {
        "parser": "manual",
        "duration_seconds": duration,
        "result": result
    }


# ── LLM Parser ────────────────────────────────────────────

@app.post("/parse-llm")
@limiter.limit("5/minute")
def parse_llm(request: Request, data: TimetableInput):

    logger.info(f"POST /parse-llm | length={len(data.text)}")
    start = time.time()

    try:
        result = llm_parser.parse(data.text)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except llm_parser.LLMConnectionError:
        raise HTTPException(status_code=503, detail="LLM unavailable")

    except llm_parser.LLMResponseError:
        raise HTTPException(status_code=502, detail="Invalid LLM response")

    duration = round(time.time() - start, 3)

    return {
        "parser": "llm",
        "duration_seconds": duration,
        "result": result
    }


# ── Compare Endpoint ──────────────────────────────────────

@app.post("/compare")
@limiter.limit("3/minute")
def compare(request: Request, data: TimetableInput):

    logger.info(f"POST /compare | length={len(data.text)}")

    # Manual
    try:
        manual_result = manual_parser.parse(data.text)
        manual_status = "success"
    except Exception as e:
        manual_result = None
        manual_status = "failed"

    # LLM
    try:
        llm_result = llm_parser.parse(data.text)
        llm_status = "success"
    except Exception as e:
        llm_result = None
        llm_status = "failed"

    decision = evaluate(manual_result, llm_result)

    return {
        "input": data.text,
        "manual": {
            "status": manual_status,
            "result": manual_result
        },
        "llm": {
            "status": llm_status,
            "result": llm_result
        },
        "decision": decision
    }


# ── SMART PARSE (🔥 CORE FEATURE) ─────────────────────────

@app.post("/smart-parse")
@limiter.limit("3/minute")
def smart_parse(request: Request, data: TimetableInput):

    logger.info(f"POST /smart-parse | length={len(data.text)}")

    # Run both
    try:
        manual_result = manual_parser.parse(data.text)
    except Exception:
        manual_result = None

    try:
        llm_result = llm_parser.parse(data.text)
    except Exception:
        llm_result = None

    # Decision
    decision = evaluate(manual_result, llm_result)

    return {
        "input": data.text,
        "decision": decision,
        "manual_output": manual_result,
        "llm_output": llm_result
    }