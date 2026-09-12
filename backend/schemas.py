from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from backend.models import SeverityLevel, AccidentType


class AccidentBase(BaseModel):
    """Base schema for accident data"""
    location: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    state: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    accident_type: AccidentType
    severity: SeverityLevel
    casualties: int = Field(default=0, ge=0)
    injuries: int = Field(default=0, ge=0)
    fatalities: int = Field(default=0, ge=0)
    weather_condition: Optional[str] = Field(None, max_length=100)
    road_condition: Optional[str] = Field(None, max_length=100)
    time_of_day: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    contributing_factors: Optional[str] = None
    reported_by: Optional[str] = Field(None, max_length=255)

    @validator('casualties')
    def validate_casualties(cls, v, values):
        """Ensure casualties match injuries + fatalities"""
        if 'injuries' in values and 'fatalities' in values:
            expected = values['injuries'] + values['fatalities']
            if v != expected:
                return expected
        return v


class AccidentCreate(AccidentBase):
    """Schema for creating an accident record"""
    pass


class AccidentUpdate(BaseModel):
    """Schema for updating an accident record"""
    location: Optional[str] = Field(None, min_length=1, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    district: Optional[str] = Field(None, min_length=1, max_length=100)
    accident_type: Optional[AccidentType] = None
    severity: Optional[SeverityLevel] = None
    casualties: Optional[int] = Field(None, ge=0)
    injuries: Optional[int] = Field(None, ge=0)
    fatalities: Optional[int] = Field(None, ge=0)
    weather_condition: Optional[str] = Field(None, max_length=100)
    road_condition: Optional[str] = Field(None, max_length=100)
    time_of_day: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    contributing_factors: Optional[str] = None
    verified: Optional[int] = Field(None, ge=0, le=1)


class AccidentResponse(AccidentBase):
    """Schema for accident response"""
    id: int
    verified: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AccidentListResponse(BaseModel):
    """Schema for paginated accident list"""
    total: int
    page: int
    page_size: int
    accidents: list[AccidentResponse]
