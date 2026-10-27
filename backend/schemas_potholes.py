"""
Pydantic schemas for pothole detection, verification, and defect analytics.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime


class PotholeDetectionBox(BaseModel):
    box: List[int]
    confidence: float
    label: str
    relative_area: float


class PotholeDetectionResponse(BaseModel):
    pothole_id: str
    pothole_count: int
    detections: List[PotholeDetectionBox]
    avg_confidence: float
    severity: str
    severity_method: str
    severity_reason: str
    image_url: str
    annotated_image_url: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    road_name: Optional[str] = None
    state: Optional[str] = None
    verification_status: str
    repair_status: str
    model_id: str
    processing_time_ms: float
    is_demo: bool
    detection_date: datetime


class PotholeStatusUpdate(BaseModel):
    verification_status: Optional[str] = Field(None, pattern="^(unverified|verified|rejected)$")
    repair_status: Optional[str] = Field(None, pattern="^(reported|inspected|scheduled|in_progress|repaired)$")
    severity: Optional[str] = Field(None, pattern="^(minor|moderate|severe|critical)$")
    notes: Optional[str] = None


class PotholeAnalyticsResponse(BaseModel):
    total_detected: int
    total_verified: int
    high_priority_count: int
    unresolved_count: int
    repaired_count: int
    severity_distribution: Dict[str, int]
    repair_status_distribution: Dict[str, int]
    top_corridors: List[Dict[str, Any]]
    model_info: Dict[str, Any]
