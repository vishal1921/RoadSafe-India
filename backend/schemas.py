from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from backend.models import SeverityLevel, AccidentType, RoadType

class AccidentBase(BaseModel):
    location: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    state: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    corridor: Optional[str] = None
    road_type: Optional[str] = "national_highway"
    
    accident_type: AccidentType = AccidentType.COLLISION
    severity: SeverityLevel = SeverityLevel.MODERATE
    
    casualties: int = Field(0, ge=0)
    injuries: int = Field(0, ge=0)
    fatalities: int = Field(0, ge=0)
    
    weather_condition: Optional[str] = "Clear"
    road_condition: Optional[str] = "Dry"
    time_of_day: Optional[str] = "Evening"
    speed_limit: Optional[int] = 80
    observed_speed: Optional[int] = None
    
    geometry: Optional[str] = "straight"
    lighting: Optional[str] = "daylight"
    dominant_cause: Optional[str] = None
    contributing_factors: Optional[str] = None
    description: Optional[str] = None
    reported_by: Optional[str] = "Field Officer"

    @field_validator('casualties')
    @classmethod
    def casualties_match(cls, v, info):
        d = info.data
        if 'injuries' in d or 'fatalities' in d:
            calc = (d.get('injuries') or 0) + (d.get('fatalities') or 0)
            if calc > 0:
                return calc
        return v

class AccidentCreate(AccidentBase):
    pass

class AccidentUpdate(BaseModel):
    location: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    state: Optional[str] = None
    district: Optional[str] = None
    corridor: Optional[str] = None
    road_type: Optional[str] = None
    accident_type: Optional[AccidentType] = None
    severity: Optional[SeverityLevel] = None
    casualties: Optional[int] = Field(None, ge=0)
    injuries: Optional[int] = Field(None, ge=0)
    fatalities: Optional[int] = Field(None, ge=0)
    weather_condition: Optional[str] = None
    road_condition: Optional[str] = None
    time_of_day: Optional[str] = None
    speed_limit: Optional[int] = None
    observed_speed: Optional[int] = None
    geometry: Optional[str] = None
    lighting: Optional[str] = None
    dominant_cause: Optional[str] = None
    contributing_factors: Optional[str] = None
    description: Optional[str] = None
    verified: Optional[int] = Field(None, ge=0, le=1)

class AccidentResponse(AccidentBase):
    id: int
    risk_score: float
    morth_blackspot_id: Optional[str] = None
    verified: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {'from_attributes': True}

class AccidentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    accidents: List[AccidentResponse]

class DriverAttribution(BaseModel):
    factor: str
    weight: float
    category: str
    actionable_insight: str

class RiskPredictionRequest(BaseModel):
    latitude: float = 28.7041
    longitude: float = 77.1025
    road_type: str = "national_highway"
    speed_limit: int = 80
    operating_speed: int = 95
    weather: str = "Rain"
    road_condition: str = "Wet"
    time_of_day: str = "Night"
    geometry: str = "sharp_curve"
    lighting: str = "poor_lighting"
    vulnerable_user_density: str = "high"

class RiskPredictionResponse(BaseModel):
    risk_score: float
    risk_band: str
    confidence: float
    lethality_index: float
    dominant_hazard: str
    drivers: List[DriverAttribution]
    recommended_speed: int
    recommended_first_response: str

class CounterfactualSimulationRequest(BaseModel):
    baseline_risk: float = 82.0
    baseline_fatalities_annual: int = 30
    baseline_crashes_annual: int = 45
    selected_interventions: List[str]

class CounterfactualSimulationResponse(BaseModel):
    baseline_risk: float
    simulated_risk: float
    risk_reduction_pct: float
    crashes_prevented_annual: int
    lives_saved_annual: int
    injuries_prevented_annual: int
    safety_roi_rating: str
    interventions_applied: List[Dict[str, Any]]
