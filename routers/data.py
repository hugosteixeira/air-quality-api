from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from database import get_db
from Model.reading import Reading
from Model.readerDevice import ReaderDevice
from datetime import datetime, timedelta
from typing import List, Union  # Added Union for mixed types
from pydantic import BaseModel  # Import BaseModel for request body validation

router = APIRouter()

class DeviceIdsRequest(BaseModel):  # Define a Pydantic model for the request body
    device_ids: Union[int, List[int]]

class ReadingsRequest(BaseModel):  # Define a Pydantic model for the request body
    skip: int = 0
    limit: int = 10
    start_ts: str = None
    end_ts: str = None
    device_ids: Union[int, List[int]] = None
    reading_type: str = None

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

@router.post("/readings")  # Add POST method for /readings
def get_readings_post(
    request: ReadingsRequest,  # Accept filters in the request body
    db: Session = Depends(get_db)
):
    filters = []
    if request.start_ts and request.end_ts:
        start_date = datetime.strptime(request.start_ts, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(request.end_ts, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=1)
        filters.append(and_(Reading.ts >= start_date, Reading.ts < end_date))
    if request.device_ids:
        device_ids = [request.device_ids] if isinstance(request.device_ids, int) else request.device_ids
        filters.append(Reading.device_id.in_(device_ids))
    if request.reading_type:
        filters.append(Reading.reading_type == request.reading_type)
    
    query = db.query(Reading).filter(*filters)
    
    total_count = query.count()
    if request.limit > 0:
        query = query.offset(request.skip).limit(request.limit)
    readings = query.all()
    return {
        "total_count": total_count,
        "readings": readings
    }

@router.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    devices = db.query(ReaderDevice).all()
    return [{"id": device.id, "name": device.name, "latitude": device.latitude, "longitude": device.longitude} for device in devices]

@router.post("/readings/latest")  # Change to POST
def get_latest_instant_reading(
    request: DeviceIdsRequest,  # Accept device_ids in the request body
    db: Session = Depends(get_db)
):
    device_ids = request.device_ids
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
