from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
from datetime import datetime
import enum

from backend.database import Base


class SeverityLevel(str, enum.Enum):
    """Accident severity levels"""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    FATAL = "fatal"


class AccidentType(str, enum.Enum):
    """Types of accidents"""
    COLLISION = "collision"
    PEDESTRIAN = "pedestrian"
    VEHICLE_ROLLOVER = "vehicle_rollover"
    HEAD_ON = "head_on"
    REAR_END = "rear_end"
    SIDE_IMPACT = "side_impact"
    OTHER = "other"


class Accident(Base):
    """Accident record model"""
    __tablename__ = "accidents"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    state = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    
    accident_type = Column(Enum(AccidentType), nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False, index=True)
    
    casualties = Column(Integer, default=0)
    injuries = Column(Integer, default=0)
    fatalities = Column(Integer, default=0)
    
    weather_condition = Column(String(100))
    road_condition = Column(String(100))
    time_of_day = Column(String(50))
    
    description = Column(Text)
    contributing_factors = Column(Text)
    
    reported_by = Column(String(255))
    verified = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Accident(id={self.id}, location={self.location}, severity={self.severity})>"
