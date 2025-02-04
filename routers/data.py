from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from database import get_db
from Model.reading import Reading
from Model.readerDevice import ReaderDevice

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
        filters.append(and_(Reading.ts >= start_ts, Reading.ts <= end_ts))
    if device_id:
        filters.append(Reading.device_id == device_id)
    if reading_type:
        filters.append(Reading.reading_type == reading_type)
    
    query = db.query(Reading).filter(*filters)
    query = query.offset(skip).limit(limit)
    readings = query.all()
    return readings

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
