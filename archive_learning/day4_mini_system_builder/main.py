from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

app = FastAPI()

# ENDPOINT 1 -> /calculate
@app.get("/calculate")
def calculate(num1: float, num2: float, operation: str):

    # STEP 1: check the operation is valid

    allowed_operations = ["add", "subtract", "multiply", "divide"]

    if operation not in allowed_operations:
        raise HTTPException(
            status_code=400,
            detail=f"operation must be one of: {allowed_operations}"
        )
    
    # STEP 2: check for division by zero before dividing

    if operation == "divide" and num2 == 0:
        raise HTTPException(
            status_code=400,
            detail="cannot divide by zero"
        )
    
    # STEP 3: do the actual calculation
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        result = num1 / num2
    return{"result": result}

# ENDPOINT 2 -> /day

@app.get("/day")
def get_day(number: int):

    # STEP 1: validate the range
    
    if number < 1 or number > 7:
        raise HTTPException(
            status_code=400,
            detail="number must be between 1 and 7"
        )
    
    # STEP 2: map number to day

    day = {
        1:"monday",
        2:"tuesday",
        3:"wednesday",
        4:"thursday",
        5:"friday",
        6:"saturday",
        7:"sunday"
    }
    return{"day": day[number]}

# ENDPOINT 3 -> /reverse
 
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/reverse")
def reverse_text(text: str):

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )
    
    if len(text) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Text too long. Maximum 1000 characters"
        )
    
    reversed_text = text[::-1]

    return {"reversed": reversed_text}


# part 2: the real project(/parse-timetable)

@app.get("/timetable")
def get_timetable():

    timetable = {
        "monday":[
            {"time": "9am", "subject": "math"},
            {"time": "11am", "subject": "physics"}
        ],
        "tuesday":[
            {"time": "9am", "subject": "chemistry"}
        ]
    }
    return timetable


# pydantic model

class TimetableInput(BaseModel):
    text: str

    @classmethod
    @validator("text")
    def validate(cls, value):
        if not value.strip():
            raise ValueError("text cannot be empty")
        if len(value) > 5000:
            raise ValueError("text too long")
        return value
    
# parser function
def parse_timetable(raw_text: str) -> dict:

    day_look = {
        "mon": "Monday", "monday": "Monday",
        "tue": "Tuesday", "tuesday": "Tuesday",
        "wed": "Wednesday", "wednesday": "Wednesday",
        "thu": "Thursday", "thursday": "Thursday",
        "fri": "Friday", "friday": "Friday",
        "sat": "Saturday", "saturday": "Saturday",
        "sun": "Sunday", "sunday": "Sunday"
    }
    result = {}
    entries = raw_text.split(",")

    for entry in entries:
        entry = entry.strip()

        if not entry:
            continue
        parts = entry.split()

        if len(parts) < 3:
            raise ValueError(f"Entry '{entry}' needs day, time and subject")
        raw_day = parts[0].lower()
        day = day_look.get(raw_day)

        if day is None:
            raise ValueError(f"'{parts[0]}' is not a recognized day")
        
        # handle "9 am"
        if len(parts) > 2 and parts[2].lower() in ["am","pm"]:
            time = parts[1] + parts[2]
            subject = " ".join(parts[3:])
        else:
            time = parts[1]
            subject = " ".join(parts[2:])

        if day not in result:
            result[day] = []

        result[day].append({
            "time": time,
            "subject": subject
        })
        return result
    

# ENDPOINT 5 -> /parse-timetable(POST)

@app.post("/parse-timetable")
def parse_timetable_endpoint(data: TimetableInput):

    try:
        return parse_timetable(data.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))