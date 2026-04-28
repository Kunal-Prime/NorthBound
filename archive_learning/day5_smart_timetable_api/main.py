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

import systems.smart_timetable_api.parsers.manual_parser as manual_parser
import systems.smart_timetable_api.parsers.llm_parser as llm_parser

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
    title="Timetable Parser API",
    description="Converts raw timetable text into structured JSON using manual or LLM parsing",
    version="1.0"
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
        "message": "Timetable Parser API",
        "version": "1.0",
        "endpoints": {
            "POST /parse-manual": "Rule-based parser",
            "POST /parse-llm": "AI-powered parser",
            "POST /compare": "Run both and compare",
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
        health["checks"]["llm"] = f"unreachable"
        health["status"] = "degraded"
        logger.error(f"Health check LLM failed: {e}")

    return health


@app.post("/parse-manual")
@limiter.limit("30/minute")
def parse_manual(request: Request, data: TimetableInput):
    """Parse using rule-based manual parser"""

    logger.info(f"POST /parse-manual | length={len(data.text)}")
    start = time.time()

    try:
        result = manual_parser.parse(data.text)
    except ValueError as e:
        logger.warning(f"Manual parse failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    duration = round(time.time() - start, 3)
    logger.info(f"POST /parse-manual | success | {duration}s")

    return {
        "parser": "manual",
        "duration_seconds": duration,
        "result": result
    }


@app.post("/parse-llm")
@limiter.limit("5/minute")
def parse_llm(request: Request, data: TimetableInput):
    """Parse using Gemini LLM"""

    logger.info(f"POST /parse-llm | length={len(data.text)}")
    start = time.time()

    try:
        result = llm_parser.parse(data.text)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except llm_parser.LLMConnectionError as e:
        logger.error(f"LLM unreachable: {e}")
        raise HTTPException(
            status_code=503,
            detail="LLM service unavailable. Try again later."
        )

    except llm_parser.LLMResponseError as e:
        logger.error(f"LLM bad response: {e}")
        raise HTTPException(
            status_code=502,
            detail="LLM returned unexpected response. Try again."
        )

    duration = round(time.time() - start, 3)
    logger.info(f"POST /parse-llm | success | {duration}s")

    return {
        "parser": "llm",
        "duration_seconds": duration,
        "result": result
    }


@app.post("/compare")
@limiter.limit("3/minute")
def compare(request: Request, data: TimetableInput):
    """Run both parsers. Compare results."""

    logger.info(f"POST /compare | length={len(data.text)}")

    # Manual
    try:
        manual_result = manual_parser.parse(data.text)
        manual_status = "success"
        manual_error = None
    except ValueError as e:
        manual_result = None
        manual_status = "failed"
        manual_error = str(e)

    # LLM
    try:
        llm_result = llm_parser.parse(data.text)
        llm_status = "success"
        llm_error = None
    except llm_parser.LLMConnectionError:
        llm_result = None
        llm_status = "failed"
        llm_error = "LLM service unavailable"
    except llm_parser.LLMResponseError as e:
        llm_result = None
        llm_status = "failed"
        llm_error = str(e)
    except Exception as e:
        llm_result = None
        llm_status = "failed"
        llm_error = str(e)

    return {
        "input": data.text,
        "manual_parser": {
            "status": manual_status,
            "error": manual_error,
            "result": manual_result
        },
        "llm_parser": {
            "status": llm_status,
            "error": llm_error,
            "result": llm_result
        }
    }