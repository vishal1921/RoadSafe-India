from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
import enum
from backend.database import Base

class SeverityLevel(str, enum.Enum):
    MINOR = 'minor'
    MODERATE = 'moderate'
    SEVERE = 'severe'
    FATAL = 'fatal'

class AccidentType(str, enum.Enum):
    COLLISION = 'collision'
    PEDESTRIAN = 'pedestrian'
    VEHICLE_ROLLOVER = 'vehicle_rollover'
    HEAD_ON = 'head_on'
    REAR_END = 'rear_end'
    SIDE_IMPACT = 'side_impact'
    OTHER = 'other'

class RoadType(str, enum.Enum):
    NATIONAL_HIGHWAY = 'national_highway'
    STATE_HIGHWAY = 'state_highway'
    EXPRESSWAY = 'expressway'
    URBAN_ARTERIAL = 'urban_arterial'
    RURAL_ROAD = 'rural_road'

class Accident(Base):
    __tablename__ = 'accidents'
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    state = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    corridor = Column(String(150), nullable=True)
    road_type = Column(String(50), default='national_highway', index=True)
    
    accident_type = Column(Enum(AccidentType), nullable=False, default=AccidentType.COLLISION)
    severity = Column(Enum(SeverityLevel), nullable=False, index=True, default=SeverityLevel.MODERATE)
    
    casualties = Column(Integer, default=0)
    injuries = Column(Integer, default=0)
    fatalities = Column(Integer, default=0)
    
    weather_condition = Column(String(100), default='Clear')
    road_condition = Column(String(100), default='Dry')
    time_of_day = Column(String(50), default='Evening')
    speed_limit = Column(Integer, default=80)
    observed_speed = Column(Integer, nullable=True)
    
    geometry = Column(String(100), default='straight')
    lighting = Column(String(100), default='daylight')
    dominant_cause = Column(String(200), nullable=True)
    contributing_factors = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    
    risk_score = Column(Float, default=50.0)
    morth_blackspot_id = Column(String(50), nullable=True)
    reported_by = Column(String(255), default='Field Officer')
    verified = Column(Integer, default=1)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
