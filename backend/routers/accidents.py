from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
import csv
import io

from backend.database import get_db
from backend.models import Accident, SeverityLevel, AccidentType, RoadType
from backend.schemas import (
    AccidentCreate, 
    AccidentUpdate, 
    AccidentResponse, 
    AccidentListResponse,
    RiskPredictionRequest,
    RiskPredictionResponse,
    CounterfactualSimulationRequest,
    CounterfactualSimulationResponse
)
from backend.analytics import (
    dashboard_stats, 
    get_hotspots, 
    seed_demo, 
    get_causes_analysis,
    get_vulnerability_analysis,
    get_temporal_analysis,
    get_interventions_catalog,
    get_trauma_centers,
    get_all_states,
    get_state_dossier,
    get_50year_historical_trends,
    get_junction_control_analysis,
    get_police_blackspots_registry,
    get_highways_network
)
from backend.ml_engine import ml_engine

router = APIRouter()

@router.post('/', response_model=AccidentResponse, status_code=201)
def create_accident(accident: AccidentCreate, db: Session = Depends(get_db)):
    data = accident.model_dump()
    
    # Calculate calibrated risk score
    rf = ml_engine.calculate_risk_score(
        latitude=data["latitude"],
        longitude=data["longitude"],
        road_type=data.get("road_type") or "national_highway",
        speed_limit=data.get("speed_limit") or 80,
        operating_speed=data.get("observed_speed") or (data.get("speed_limit") or 80) + 12,
        weather=data.get("weather_condition") or "Clear",
        road_condition=data.get("road_condition") or "Dry",
        time_of_day=data.get("time_of_day") or "Evening",
        geometry=data.get("geometry") or "straight",
        lighting=data.get("lighting") or "daylight",
        vulnerable_user_density="critical" if data.get("accident_type") == AccidentType.PEDESTRIAN else "high"
    )
    
    data["risk_score"] = rf["risk_score"]
    if not data.get("dominant_cause"):
        data["dominant_cause"] = rf["dominant_hazard"]
        
    obj = Accident(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get('/', response_model=AccidentListResponse)
def list_accidents(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    state: Optional[str] = None,
    district: Optional[str] = None,
    road_type: Optional[str] = None,
    severity: Optional[SeverityLevel] = None,
    accident_type: Optional[AccidentType] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Accident)
    if state and state.strip() and state.lower() != "all":
        q = q.filter(func.lower(Accident.state) == state.lower().strip())
    if district and district.strip():
        q = q.filter(func.lower(Accident.district) == district.lower().strip())
    if road_type and road_type.strip() and road_type.lower() != "all":
        q = q.filter(func.lower(Accident.road_type) == road_type.lower().strip())
    if severity:
        q = q.filter(Accident.severity == severity)
    if accident_type:
        q = q.filter(Accident.accident_type == accident_type)

    total = q.count()
    rows = q.order_by(Accident.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {'total': total, 'page': page, 'page_size': page_size, 'accidents': rows}

@router.get('/stats/summary')
def summary(state: Optional[str] = None, db: Session = Depends(get_db)):
    """Summary KPI statistics for National / State Command Center"""
    return dashboard_stats(db, state)

@router.get('/analytics/hotspots')
def hotspots_endpoint(state: Optional[str] = None, road_type: Optional[str] = None, db: Session = Depends(get_db)):
    """Question 1: Where are accidents most likely to occur? Returns ranked geocoded blackspots."""
    return get_hotspots(db, state, road_type)

@router.get('/analytics/risk')
def calculate_risk_get(
    latitude: float = 28.7041,
    longitude: float = 77.1025,
    road_type: str = "national_highway",
    speed_limit: int = 80,
    operating_speed: int = 95,
    weather: str = 'Rain',
    road_condition: str = 'Wet',
    time_of_day: str = 'Evening',
    geometry: str = 'sharp_curve',
    lighting: str = 'poor_lighting',
    vulnerable_user_density: str = 'high'
):
    """Question 2: Why are accidents occurring there? Explainable AI 0-100 scoring & attribution."""
    return ml_engine.calculate_risk_score(
        latitude=latitude,
        longitude=longitude,
        road_type=road_type,
        speed_limit=speed_limit,
        operating_speed=operating_speed,
        weather=weather,
        road_condition=road_condition,
        time_of_day=time_of_day,
        geometry=geometry,
        lighting=lighting,
        vulnerable_user_density=vulnerable_user_density
    )

@router.post('/analytics/predict-segment', response_model=RiskPredictionResponse)
def predict_segment_post(req: RiskPredictionRequest):
    """Predict risk for any prospective or audited road segment."""
    return ml_engine.calculate_risk_score(
        latitude=req.latitude,
        longitude=req.longitude,
        road_type=req.road_type,
        speed_limit=req.speed_limit,
        operating_speed=req.operating_speed,
        weather=req.weather,
        road_condition=req.road_condition,
        time_of_day=req.time_of_day,
        geometry=req.geometry,
        lighting=req.lighting,
        vulnerable_user_density=req.vulnerable_user_density
    )

@router.get('/analytics/states')
def states_analysis_endpoint():
    """All 36 Indian States & UTs ranked with longitudinal crash metrics."""
    states = get_all_states()
    national_crashes_2023 = sum(s.get('accidents_2023', 0) for s in states)
    national_fatalities_2023 = sum(s.get('fatalities_2023', 0) for s in states)
    national_injuries_2023 = sum(s.get('injuries_2023', 0) for s in states)
    return {
        'total_entities': len(states),
        'national_crashes_2023': national_crashes_2023,
        'national_fatalities_2023': national_fatalities_2023,
        'national_injuries_2023': national_injuries_2023,
        'states': states
    }

@router.get('/analytics/states/{state_name}')
def state_dossier_endpoint(state_name: str, db: Session = Depends(get_db)):
    """In-depth state safety dossier including identified blackspots and regional IRC priorities."""
    return get_state_dossier(state_name, db)

@router.get('/analytics/historical-50yr')
def historical_trends_endpoint():
    """MoRTH 50-Year Longitudinal Road Accident & Motorization Trends (1970-2019)."""
    return get_50year_historical_trends()

@router.get('/analytics/junction-control')
def junction_control_endpoint(city: Optional[str] = None):
    """Intersection Traffic Control & Signalization Crash Distribution across 50 Million-Plus Cities."""
    return get_junction_control_analysis(city)

@router.get('/analytics/police-blackspots')
def police_blackspots_endpoint(state: Optional[str] = None, query: Optional[str] = None, limit: int = Query(100, ge=1, le=500)):
    """MoRTH Official Police Station Blackspot Registry (2016-2018 3-Year Audited Records)."""
    return get_police_blackspots_registry(state, query, limit)

@router.get('/analytics/highways')
def highways_network_endpoint(risk_level: Optional[str] = None, state: Optional[str] = None):
    """Color-coded Indian Highway Network (Green=Safe, Yellow=Low, Orange=Moderate, Red=Extreme)."""
    return get_highways_network(risk_level, state)

@router.get('/analytics/causes')
def causes_analysis_endpoint(state: Optional[str] = None):
    """Question 2: Why are accidents occurring there? MoRTH Cause breakdown."""
    return get_causes_analysis(state)

@router.get('/analytics/vulnerability')
def vulnerability_endpoint():
    """Question 3: Who/what is most vulnerable? Mode of transport and VRU breakdown."""
    return get_vulnerability_analysis()

@router.get('/analytics/temporal')
def temporal_endpoint():
    """Question 4: When is the risk highest? 24h hourly diurnal curve & seasonal factors."""
    return get_temporal_analysis()

@router.get('/analytics/prediction')
def prediction_endpoint(state: Optional[str] = None, horizon_days: int = Query(90, ge=30, le=180)):
    """Question 4 & Prediction: 30, 60, 90-day future risk forecasting."""
    return ml_engine.forecast_risk(state, horizon_days)

@router.get('/analytics/interventions')
def interventions_endpoint():
    """Question 5: What intervention should be implemented first? Ranked IRC interventions."""
    return get_interventions_catalog()

@router.post('/analytics/simulate', response_model=CounterfactualSimulationResponse)
def simulate_counterfactual_endpoint(req: CounterfactualSimulationRequest):
    """Question 6: Can we predict whether the intervention will reduce accidents? Interactive what-if simulator."""
    return ml_engine.simulate_counterfactual(
        selected_interventions=req.selected_interventions,
        baseline_risk=req.baseline_risk,
        baseline_fatalities=req.baseline_fatalities_annual,
        baseline_crashes=req.baseline_crashes_annual
    )

@router.get('/analytics/route-risk')
def route_risk_endpoint(origin: str = Query("Delhi"), destination: str = Query("Agra")):
    """Safe Routing: Assesses route hazard between cities, blackspots along corridor, and safety advisories."""
    return ml_engine.evaluate_route_hazard(origin, destination)

@router.get('/analytics/trauma-centers')
def trauma_centers_endpoint(latitude: Optional[float] = None, longitude: Optional[float] = None):
    """Golden Hour Emergency Trauma Centers & ambulance response dispatch."""
    return get_trauma_centers(latitude, longitude)

@router.post('/seed-demo')
def seed(db: Session = Depends(get_db)):
    """Populates database with 74+ geocoded Indian National Highway and Urban Blackspots."""
    return {'inserted': seed_demo(db), 'message': 'National Blackspots & Corridors successfully loaded into intelligence base.'}

@router.post('/import-csv')
def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Import CSV file containing accident records."""
    raw = file.file.read().decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(raw))
    inserted = 0
    errors = []
    
    for i, row in enumerate(reader, start=2):
        try:
            def g(*keys, default=''):
                for k in keys:
                    if row.get(k) not in (None, ''):
                        return row[k]
                return default

            lat = float(g('latitude', 'Latitude'))
            lon = float(g('longitude', 'Longitude'))
            state = g('state', 'State', default='National Corridor')
            district = g('district', 'District', default='District Central')
            location = g('location', 'Location', default=f'Incident #{i}')
            
            inj = int(float(g('injuries', 'Injuries', default='0') or 0))
            fat = int(float(g('fatalities', 'Fatalities', default='0') or 0))
            cas = int(float(g('casualties', 'Casualties', default='0') or (inj + fat)))
            
            typ_str = g('accident_type', 'Accident Type', 'accident type', default='collision').lower().replace(' ', '_')
            try:
                typ = AccidentType(typ_str)
            except Exception:
                typ = AccidentType.COLLISION
                
            sev_str = g('severity', 'Severity', default='moderate').lower()
            try:
                sev = SeverityLevel(sev_str)
            except Exception:
                sev = SeverityLevel.MODERATE
                
            weather = g('weather_condition', 'Weather', default='Clear')
            road_cond = g('road_condition', 'Road Condition', default='Dry')
            time_of_day = g('time_of_day', 'Time of Day', default='Evening')
            corridor = g('corridor', 'Corridor', default='National Highway')
            factors = g('contributing_factors', 'Cause', 'Causes', default='Speeding')
            
            # Calibrate ML risk score
            rf = ml_engine.calculate_risk_score(lat, lon, weather=weather, road_condition=road_cond, time_of_day=time_of_day)

            obj = Accident(
                location=location,
                latitude=lat,
                longitude=lon,
                state=state,
                district=district,
                corridor=corridor,
                road_type='national_highway',
                accident_type=typ,
                severity=sev,
                casualties=cas,
                injuries=inj,
                fatalities=fat,
                weather_condition=weather,
                road_condition=road_cond,
                time_of_day=time_of_day,
                dominant_cause=factors.split(';')[0] if factors else rf['dominant_hazard'],
                contributing_factors=factors,
                description=f"Imported from CSV audit record #{i}",
                risk_score=rf["risk_score"],
                reported_by='CSV Audit Import',
                verified=1
            )
            db.add(obj)
            inserted += 1
        except Exception as e:
            errors.append({'row': i, 'error': str(e)})
            
    db.commit()
    return {'inserted': inserted, 'errors': errors[:20]}

@router.get('/{accident_id}', response_model=AccidentResponse)
def get_accident(accident_id: int, db: Session = Depends(get_db)):
    obj = db.query(Accident).filter(Accident.id == accident_id).first()
    if not obj:
        raise HTTPException(404, 'Accident not found')
    return obj

@router.put('/{accident_id}', response_model=AccidentResponse)
def update_accident(accident_id: int, data: AccidentUpdate, db: Session = Depends(get_db)):
    obj = db.query(Accident).filter(Accident.id == accident_id).first()
    if not obj:
        raise HTTPException(404, 'Accident not found')
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete('/{accident_id}', status_code=204)
def delete_accident(accident_id: int, db: Session = Depends(get_db)):
    obj = db.query(Accident).filter(Accident.id == accident_id).first()
    if not obj:
        raise HTTPException(404, 'Accident not found')
    db.delete(obj)
    db.commit()
