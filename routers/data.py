from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from database import get_db
from Model.reading import Reading
from Model.readerDevice import ReaderDevice
from datetime import datetime, timedelta
from typing import List, Union  # Added Union for mixed types

router = APIRouter()

@router.get("/readings")
def get_readings(
    skip: int = 0, 
    limit: int = 10, 
    start_ts: str = None, 
    end_ts: str = None, 
    device_ids: List[int] = None,  # Changed to accept a list of device IDs
    reading_type: str = None, 
    db: Session = Depends(get_db)
):
    filters = []
    if start_ts and end_ts:
        start_date = datetime.strptime(start_ts, "%Y-%m-%d")
        end_date = datetime.strptime(end_ts, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
        filters.append(and_(Reading.ts >= start_date, Reading.ts <= end_date))
    if device_ids:
        filters.append(Reading.device_id.in_(device_ids))  # Updated to filter by a list of device IDs
    if reading_type:
        filters.append(Reading.reading_type == reading_type)
    
    query = db.query(Reading).filter(*filters)
    
    total_count = query.count()
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
    return [{"id": device.id, "name": device.name, "latitude": device.latitude, "longitude": device.longitude} for device in devices]

@router.get("/readings/latest")
def get_latest_instant_reading(
    device_ids: Union[int, List[int]],  # Accept either a single device_id or a list of device_ids
    db: Session = Depends(get_db)
):
    if isinstance(device_ids, int):  # Convert single device_id to a list
        device_ids = [device_ids]

    latest_readings = []
    for device_id in device_ids:
        latest_reading = db.query(Reading).filter(
            Reading.device_id == device_id,
            Reading.reading_type == "instant"
        ).order_by(Reading.ts.desc()).first()
        if latest_reading:
            latest_readings.append(latest_reading)
    
    if latest_readings:
        return latest_readings
    else:
        return {"message": "No instant readings found for the specified devices."}
