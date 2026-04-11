from fastapi import FastAPI
from datetime import datetime
import pytz
from pydantic import BaseModel

app = FastAPI()

# -------------------------
# Endpoint 1: Home / Greet
# -------------------------
@app.get("/")
def home():
    return {"message": "I am alive"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"greeting": f"Hello {name}, welcome"}

# -------------------------
# Endpoint 2: Calculate
# -------------------------
class Numbers(BaseModel):
    a: float
    b: float

@app.post("/calculate")
def calculate(data: Numbers):
    return {
        "sum": data.a + data.b,
        "difference": data.a - data.b,
        "product": data.a * data.b,
        "division": data.a / data.b if data.b != 0 else "Cannot divide by zero"
    }

# -------------------------
# Endpoint 3: Day / Time
# -------------------------
@app.get("/day")
def get_day():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return {
        "day": now.strftime("%A"),
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%I:%M %p"),
        "timezone": "IST"
    }

# Endpoint 4: Reverse

class TextInput(BaseModel):
    text: str

@app.post("/reverse")
def reverse(data: TextInput):
    return{
        "original": data.text,
        "reversed": data.text[::-1],
        "length": len(data.text)
    }