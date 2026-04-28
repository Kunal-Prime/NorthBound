from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.timetable import Timetable
from app.database import get_db   # we'll create this next

router = APIRouter(prefix="/timetables", tags=["timetables"])

class TimetableCreate(BaseModel):
    title: str
    data: str

@router.post("/parse-and-save")
def parse_and_save(timetable: TimetableCreate, db: Session = Depends(get_db)):
    """Parse timetable and persist it to database."""
    db_timetable = Timetable(title=timetable.title, data=timetable.data)
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return {"id": db_timetable.id, "message": "Timetable saved successfully"}

@router.get("/")
def list_timetables(db: Session = Depends(get_db)):
    """Return all saved timetables."""
    return db.query(Timetable).all()

@router.get("/{timetable_id}")
def get_timetable(timetable_id: int, db: Session = Depends(get_db)):
    """Get a single timetable by ID."""
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if timetable is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return timetable