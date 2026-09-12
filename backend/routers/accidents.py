from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from backend.database import get_db
from backend.models import Accident, SeverityLevel, AccidentType
from backend.schemas import AccidentCreate, AccidentUpdate, AccidentResponse, AccidentListResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=AccidentResponse, status_code=201)
def create_accident(
    accident: AccidentCreate,
    db: Session = Depends(get_db)
):
    """Create a new accident record"""
    try:
        db_accident = Accident(**accident.model_dump())
        db.add(db_accident)
        db.commit()
        db.refresh(db_accident)
        logger.info(f"Created accident record: {db_accident.id}")
        return db_accident
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating accident: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create accident record")


@router.get("/", response_model=AccidentListResponse)
def list_accidents(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    state: Optional[str] = None,
    district: Optional[str] = None,
    severity: Optional[SeverityLevel] = None,
    accident_type: Optional[AccidentType] = None,
    db: Session = Depends(get_db)
):
    """List accidents with pagination and filters"""
    try:
        query = db.query(Accident)
        
        # Apply filters
        if state:
            query = query.filter(Accident.state == state)
        if district:
            query = query.filter(Accident.district == district)
        if severity:
            query = query.filter(Accident.severity == severity)
        if accident_type:
            query = query.filter(Accident.accident_type == accident_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        accidents = query.order_by(Accident.created_at.desc()).offset(offset).limit(page_size).all()
        
        return AccidentListResponse(
            total=total,
            page=page,
            page_size=page_size,
            accidents=accidents
        )
    except Exception as e:
        logger.error(f"Error listing accidents: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve accidents")


@router.get("/{accident_id}", response_model=AccidentResponse)
def get_accident(
    accident_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific accident by ID"""
    accident = db.query(Accident).filter(Accident.id == accident_id).first()
    if not accident:
        raise HTTPException(status_code=404, detail="Accident not found")
    return accident


@router.put("/{accident_id}", response_model=AccidentResponse)
def update_accident(
    accident_id: int,
    accident_update: AccidentUpdate,
    db: Session = Depends(get_db)
):
    """Update an accident record"""
    try:
        db_accident = db.query(Accident).filter(Accident.id == accident_id).first()
        if not db_accident:
            raise HTTPException(status_code=404, detail="Accident not found")
        
        # Update only provided fields
        update_data = accident_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_accident, field, value)
        
        db.commit()
        db.refresh(db_accident)
        logger.info(f"Updated accident record: {accident_id}")
        return db_accident
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating accident: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update accident record")


@router.delete("/{accident_id}", status_code=204)
def delete_accident(
    accident_id: int,
    db: Session = Depends(get_db)
):
    """Delete an accident record"""
    try:
        db_accident = db.query(Accident).filter(Accident.id == accident_id).first()
        if not db_accident:
            raise HTTPException(status_code=404, detail="Accident not found")
        
        db.delete(db_accident)
        db.commit()
        logger.info(f"Deleted accident record: {accident_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting accident: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete accident record")


@router.get("/stats/summary")
def get_accident_statistics(
    state: Optional[str] = None,
    district: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get accident statistics summary"""
    try:
        query = db.query(Accident)
        
        if state:
            query = query.filter(Accident.state == state)
        if district:
            query = query.filter(Accident.district == district)
        
        total_accidents = query.count()
        total_fatalities = db.query(func.sum(Accident.fatalities)).filter(
            Accident.state == state if state else True,
            Accident.district == district if district else True
        ).scalar() or 0
        total_injuries = db.query(func.sum(Accident.injuries)).filter(
            Accident.state == state if state else True,
            Accident.district == district if district else True
        ).scalar() or 0
        
        severity_breakdown = {}
        for severity in SeverityLevel:
            count = query.filter(Accident.severity == severity).count()
            severity_breakdown[severity.value] = count
        
        return {
            "total_accidents": total_accidents,
            "total_fatalities": int(total_fatalities),
            "total_injuries": int(total_injuries),
            "severity_breakdown": severity_breakdown,
            "filters_applied": {
                "state": state,
                "district": district
            }
        }
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


from sqlalchemy import func
