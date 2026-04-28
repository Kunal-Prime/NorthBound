from fastapi import FastAPI
from app.routes.timetables import router as timetables_router
from app.models.timetable import Base
from app.database import engine
import os

app = FastAPI(title="Timetable API", version="1.0.0")

# Create tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.include_router(timetables_router)