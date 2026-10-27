from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum, Boolean
from sqlalchemy.sql import func
import enum
from backend.database import Base


class User(Base):
    """User model for authentication and role-based access control"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False, default='user')  # 'user', 'contractor', 'government'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

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


class PotholeRecord(Base):
    """Pothole detection and road defect intelligence record"""
    __tablename__ = 'pothole_records'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pothole_id = Column(String(50), unique=True, nullable=False, index=True)
    detection_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    image_path = Column(String(255), nullable=False)
    annotated_image_path = Column(String(255), nullable=True)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    road_name = Column(String(150), nullable=True, index=True)
    state = Column(String(100), nullable=True, index=True)
    district = Column(String(100), nullable=True)
    
    pothole_count = Column(Integer, default=0, nullable=False)
    bounding_boxes_json = Column(Text, nullable=True)  # JSON array of bounding boxes
    detection_confidence = Column(Float, default=0.0)
    
    severity = Column(String(50), default='moderate', index=True)  # minor, moderate, severe, critical
    severity_method = Column(String(200), default='Heuristic Rule: Relative Frame Area & Multi-Defect Co-occurrence')
    severity_reason = Column(Text, nullable=True)
    
    verification_status = Column(String(50), default='unverified', index=True)  # unverified, verified, rejected
    repair_status = Column(String(50), default='reported', index=True)  # reported, inspected, scheduled, in_progress, repaired
    
    reporter = Column(String(100), default='RoadSafe Vision AI')
    model_id = Column(String(100), default='pothole-vision-adapter-v1')
    processing_time_ms = Column(Float, default=0.0)
    is_demo = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
