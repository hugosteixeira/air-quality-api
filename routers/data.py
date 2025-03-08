from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from database import get_db
from Model.reading import Reading
from Model.readerDevice import ReaderDevice
from datetime import datetime

router = APIRouter()

@router.get("/readings")
def get_readings(
    skip: int = 0, 
    limit: int = 10, 
    start_ts: str = None, 
    end_ts: str = None, 
    device_id: int = None, 
    reading_type: str = None, 
    db: Session = Depends(get_db)
):
    filters = []
    if start_ts and end_ts:
        start_date = datetime.strptime(start_ts, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_ts, "%Y-%m-%d").date()
        filters.append(and_(func.date(Reading.ts) >= start_date, func.date(Reading.ts) <= end_date))
    if device_id:
        filters.append(Reading.device_id == device_id)
    if reading_type:
        filters.append(Reading.reading_type == reading_type)
    
    query = db.query(Reading).filter(*filters)
    
    total_count = query.count()  # Get the total count of records
    if limit > 0:
        query = query.offset(skip).limit(limit)
    readings = query.all()
    return {
        "total_count": total_count,
        "readings": readings
    }

@router.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(ReaderDevice).all()
    return [{"id": device.id, "name": device.name} for device in devices]

@router.get("/readings/latest")
def get_latest_instant_reading(device_id: int, db: Session = Depends(get_db)):
    latest_reading = db.query(Reading).filter(
        Reading.device_id == device_id,
        Reading.reading_type == "instant"
    ).order_by(Reading.ts.desc()).first()
    
    if latest_reading:
        return latest_reading
    else:
        return {"message": "No instant readings found for the specified device."}
