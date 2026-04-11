import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

# Create model once
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are a timetable parser.

Convert the raw timetable text into structured JSON.

Rules:
- Return ONLY valid JSON. No explanation. No markdown. No code blocks.
- Convert short day names to full names (mon → Monday, tue → Tuesday, etc)
- Group entries by day
- Each entry must have exactly two fields: "time" and "subject"
- If a subject has multiple words, keep them as one string
- If the input is empty or unrecognizable, return an empty object {}

Example input:
Mon 9am Math, Tue 11am Computer Science

Example output:
{"Monday": [{"time": "9am", "subject": "Math"}], "Tuesday": [{"time": "11am", "subject": "Computer Science"}]}
"""

# Custom exceptions
class LLMConnectionError(Exception):
    """Raised when we cannot reach the LLM API"""
    pass

class LLMResponseError(Exception):
    """Raised when LLM returns something we cannot use"""
    pass


def clean_llm_response(raw: str) -> str:
    """
    Remove markdown formatting if LLM added it.
    LLMs sometimes return '''json...''' even when told not to
    """
    raw = raw.strip()

    if raw.startswith("'''"):
        lines = raw.split("\n")
        lines = [line for line in lines if not line.startswith("'''")]
        raw = "\n".join(lines).strip()

    return raw


def parse(raw_text: str) -> dict:
    """
    Send text to Gemini and return structured dict.

    Raises:
        ValueError: if input is empty
        LLMConnectionError: if API is unreachable
        LLMResponseError: if response is not valid JSON
    """

    # Input check
    if not raw_text or not raw_text.strip():
        raise ValueError("Input text cannot be empty")

    full_prompt = SYSTEM_PROMPT + "\n\n Now parse this:\n" + raw_text

    # API call
    try:
        response = model.generate_content(full_prompt)
    except Exception as e:
        raise LLMConnectionError(
            f"Could not reach GEMINI API: {str(e)}"
        )

    # Get text from response
    try:
        raw_response = response.text
    except Exception:
        raise LLMConnectionError(
            "GEMINI returned an empty or malformed response"
        )

    # Clean up
    cleaned = clean_llm_response(raw_response)

    # Parse JSON
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        raise LLMResponseError(
            f"LLM returned invalid JSON. Got: {cleaned[:200]}"
        )

    # Validate structure
    if not isinstance(result, dict):
        raise LLMResponseError(
            f"Expected a JSON object, got: {type(result).__name__}"
        )

    return result