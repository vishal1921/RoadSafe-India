from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict, Any
import os
import json
import math

from backend.models import Accident, SeverityLevel, AccidentType, RoadType
from backend.ml_engine import ml_engine, INTERVENTION_CATALOG

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

def seed_demo(db: Session) -> int:
    """
    Seeds database with authentic geocoded Indian Blackspots & Corridors from data/indian_blackspots_database.json
    """
    ml_engine.reload_data()
    blackspots = ml_engine.blackspots_data
    if not blackspots:
        # Fallback to loading file directly
        json_path = os.path.join(DATA_DIR, "indian_blackspots_database.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                blackspots = json.load(f)

    existing_names = set(r[0] for r in db.query(Accident.location).all())
    inserted = 0
    for bs in blackspots:
        if bs["name"] in existing_names:
            continue
        # Compute ML risk score with target_score from calibrated database
        target_score = bs.get("risk_score")
        risk_calc = ml_engine.calculate_risk_score(
            latitude=bs["latitude"],
            longitude=bs["longitude"],
            road_type=bs.get("road_type", "national_highway"),
            speed_limit=bs.get("speed_limit", 80),
            operating_speed=bs.get("observed_avg_speed", 92),
            weather="Rain" if bs.get("surface_condition") == "wet" else "Clear",
            road_condition="Wet" if bs.get("surface_condition") == "wet" else "Dry",
            time_of_day="Evening",
            geometry=bs.get("geometry", "straight"),
            lighting=bs.get("lighting", "poor_lighting"),
            vulnerable_user_density=bs.get("vulnerable_user_density", "high"),
            target_score=target_score
        )

        final_score = target_score if target_score is not None else risk_calc["risk_score"]
        sev = SeverityLevel.FATAL if final_score >= 80.0 else SeverityLevel.SEVERE if final_score >= 60.0 else SeverityLevel.MODERATE
        typ = AccidentType.PEDESTRIAN if "Pedestrian" in bs.get("dominant_cause", "") else AccidentType.HEAD_ON if "Head-on" in bs.get("dominant_cause", "") else AccidentType.VEHICLE_ROLLOVER if "rollover" in bs.get("dominant_cause", "").lower() else AccidentType.COLLISION

        acc = Accident(
            location=bs["name"],
            latitude=bs["latitude"],
            longitude=bs["longitude"],
            state=bs["state"],
            district=bs["district"],
            corridor=bs.get("corridor", "National Highway"),
            road_type=bs.get("road_type", "national_highway"),
            accident_type=typ,
            severity=sev,
            casualties=bs.get("fatalities_3yr", 0) + bs.get("injuries_3yr", 0),
            injuries=bs.get("injuries_3yr", 0),
            fatalities=bs.get("fatalities_3yr", 0),
            weather_condition="Monsoon Rain" if bs.get("surface_condition") == "wet" else "Winter Fog" if "Fog" in bs.get("dominant_cause", "") else "Clear",
            road_condition="Wet" if bs.get("surface_condition") == "wet" else "Dry",
            time_of_day="Evening (18:00 - 21:00)",
            speed_limit=bs.get("speed_limit", 80),
            observed_speed=bs.get("observed_avg_speed", 92),
            geometry=bs.get("geometry", "straight"),
            lighting=bs.get("lighting", "poor_lighting"),
            dominant_cause=bs.get("dominant_cause", "Overspeeding"),
            contributing_factors=f"{bs.get('dominant_cause', 'Overspeeding')}; AADT: {bs.get('aadt', 80000)}; Speed Limit: {bs.get('speed_limit', 80)} km/h",
            description=f"Identified MoRTH Blackspot {bs.get('morth_blackspot_id', '')} on corridor {bs.get('corridor', '')}. 3-year casualty rate: {bs.get('historical_crashes_3yr', 0)} crashes.",
            risk_score=final_score,
            morth_blackspot_id=bs.get("morth_blackspot_id"),
            reported_by="MoRTH / NCRB National Database Adapter",
            verified=1
        )
        db.add(acc)
        inserted += 1

    db.commit()
    return db.query(Accident).count()

def get_hotspots(db: Session, state: Optional[str] = None, road_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns ranked accident blackspots with calculated ML risk scores and explainable AI feature drivers
    """
    query = db.query(Accident)
    if state and state.strip() and state.lower() != "all":
        query = query.filter(func.lower(Accident.state) == state.lower().strip())
    if road_type and road_type.strip() and road_type.lower() != "all":
        query = query.filter(func.lower(Accident.road_type) == road_type.lower().strip())

    rows = query.all()
    results = []
    
    for r in rows:
        target_score = r.risk_score
        # Run ML engine to get live explainability attribution
        rf = ml_engine.calculate_risk_score(
            latitude=r.latitude,
            longitude=r.longitude,
            road_type=r.road_type or "national_highway",
            speed_limit=r.speed_limit or 80,
            operating_speed=r.observed_speed or ((r.speed_limit or 80) + 8),
            weather=r.weather_condition or "Clear",
            road_condition=r.road_condition or "Dry",
            time_of_day=r.time_of_day or "Evening",
            geometry=r.geometry or "straight",
            lighting=r.lighting or "poor_lighting",
            vulnerable_user_density="critical" if r.accident_type == AccidentType.PEDESTRIAN else "high",
            target_score=target_score
        )
        
        final_score = round(r.risk_score if r.risk_score is not None else rf["risk_score"], 1)
        if final_score >= 80.0:
            band = "Critical"
        elif final_score >= 60.0:
            band = "High"
        else:
            band = "Moderate"

        results.append({
            "id": r.id,
            "location": r.location,
            "state": r.state,
            "district": r.district,
            "corridor": r.corridor or "Corridor",
            "road_type": r.road_type or "national_highway",
            "latitude": r.latitude,
            "longitude": r.longitude,
            "morth_blackspot_id": r.morth_blackspot_id or f"BS-{r.id:03d}",
            "risk_score": final_score,
            "risk_band": band,
            "confidence": rf["confidence"],
            "lethality_index": round(final_score * 0.88, 1),
            "dominant_hazard": rf["dominant_hazard"],
            "dominant_cause": r.dominant_cause or rf["dominant_hazard"],
            "fatalities": r.fatalities or 0,
            "injuries": r.injuries or 0,
            "casualties": r.casualties or 0,
            "speed_limit": r.speed_limit or 80,
            "observed_speed": r.observed_speed or (r.speed_limit or 80) + 8,
            "weather": r.weather_condition,
            "road_condition": r.road_condition,
            "drivers": rf["drivers"],
            "recommended_speed": rf["recommended_speed"],
            "recommended_first_response": rf["recommended_first_response"]
        })

    # Rank by risk score descending
    return sorted(results, key=lambda x: x["risk_score"], reverse=True)

def dashboard_stats(db: Session, state: Optional[str] = None) -> Dict[str, Any]:
    """
    Computes summary metrics for National Command Center
    """
    q = db.query(Accident)
    if state and state.strip() and state.lower() != "all":
        q = q.filter(func.lower(Accident.state) == state.lower().strip())
        
    rows = q.all()
    total = len(rows)
    fatalities = sum(r.fatalities or 0 for r in rows)
    injuries = sum(r.injuries or 0 for r in rows)
    critical_blackspots = sum(1 for r in rows if (r.risk_score or 0) >= 80)
    high_blackspots = sum(1 for r in rows if 60 <= (r.risk_score or 0) < 80)
    moderate_blackspots = sum(1 for r in rows if (r.risk_score or 0) < 60)

    # Estimate preventable deaths with P1+P2 interventions (~38% based on MoRTH data)
    preventable_deaths = int(round(fatalities * 0.38))

    return {
        "total_accidents": total,
        "fatalities": fatalities,
        "injuries": injuries,
        "critical_blackspots": critical_blackspots,
        "high_blackspots": high_blackspots,
        "moderate_blackspots": moderate_blackspots,
        "preventable_deaths": preventable_deaths,
        "verified": sum(1 for r in rows if r.verified),
        "severity": dict(Counter(r.severity.value for r in rows)),

        "states": dict(Counter(r.state for r in rows)),
        "road_types": dict(Counter((r.road_type or 'national_highway') for r in rows)),
        "types": dict(Counter(r.accident_type.value for r in rows)),
        "time_of_day": dict(Counter((r.time_of_day or 'Evening') for r in rows)),
        "dominant_causes": dict(Counter((r.dominant_cause or 'Overspeeding') for r in rows))
    }

def get_causes_analysis(state: Optional[str] = None) -> Dict[str, Any]:
    """
    Official MoRTH Cause of Accident Breakdown (Dataset D)
    """
    return {
        "source": "Ministry of Road Transport & Highways (MoRTH) & NCRB 2023",
        "national_causes": ml_engine.causes_data,
        "key_takeaways": [
            "Overspeeding accounts for 69.6% of road accidents and 67.4% of total road fatalities across India.",
            "Dangerous/Wrong-side driving and unsignalized median crossings contribute to 5.8% of deaths.",
            "Poor road geometry, sharp unbanked curves, and substandard intersections trigger 5.2% of fatal rollover crashes.",
            "Potholes and rutted monsoonal surfaces directly cause over 7,000 deaths annually, primarily impacting two-wheelers."
        ]
    }

def get_vulnerability_analysis() -> Dict[str, Any]:
    """
    Vulnerable Road Users (VRU) & Mode of Transport Breakdown (Dataset E)
    """
    return {
        "source": "MoRTH Transport Research Wing & NCRB ADSI 2023",
        "modes": ml_engine.modes_data,
        "vru_share_total": 64.0, # 44.5% two-wheelers + 19.5% pedestrians
        "key_takeaways": [
            "Vulnerable Road Users (Two-wheelers + Pedestrians) account for 64% of all road accident deaths in India.",
            "Two-wheelers suffer the highest fatal impact (44.5% deaths), predominantly caused by helmet non-compliance and side-swipes by heavy vehicles.",
            "Pedestrians represent 19.5% of fatalities due to absence of grade-separated crossings on 4/6-lane National Highways.",
            "Heavy commercial trucks (9.4% occupant fatalities) act as primary lethal colliding agents in 42% of multi-vehicle crashes."
        ]
    }

def get_temporal_analysis() -> Dict[str, Any]:
    """
    Diurnal 24-Hour & Seasonality Hazard Matrix
    """
    return ml_engine.temporal_data

def get_interventions_catalog() -> Dict[str, Any]:
    """
    Returns prioritized IRC-standard interventions catalog with crash modification factors
    """
    items = list(INTERVENTION_CATALOG.values())
    return {
        "guidelines": "Indian Roads Congress (IRC) & MoRTH Road Safety Audit Guidelines",
        "interventions": items
    }

def get_trauma_centers(latitude: Optional[float] = None, longitude: Optional[float] = None) -> List[Dict[str, Any]]:
    """
    Golden Hour Emergency Trauma Care Network
    """
    centers = ml_engine.trauma_data
    if latitude is not None and longitude is not None:
        for c in centers:
            dist = math.hypot(latitude - c["latitude"], longitude - c["longitude"]) * 111.0 # approx km
            c["distance_km"] = round(dist, 1)
            c["est_dispatch_minutes"] = max(5, int(round(c["distance_km"] / 45.0 * 60.0)))
        centers = sorted(centers, key=lambda x: x.get("distance_km", 999))
    return centers

def get_all_states() -> List[Dict[str, Any]]:
    """
    Returns all 36 Indian States and Union Territories ranked with complete MoRTH / NCRB analytics
    """
    states = ml_engine.morth_data
    if not states:
        json_path = os.path.join(DATA_DIR, "morth_timeseries_state_accidents.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                states = json.load(f)
                
    # Sort by fatalities descending
    ranked = sorted(states, key=lambda x: x.get("fatalities_2023", 0), reverse=True)
    for idx, s in enumerate(ranked, start=1):
        s["national_rank"] = idx
    return ranked

def get_state_dossier(state_name: str, db: Session) -> Dict[str, Any]:
    """
    Returns an in-depth road safety dossier for any state/UT
    """
    all_states = get_all_states()
    target = next((s for s in all_states if s["state"].lower() == state_name.lower().strip()), None)
    if not target:
        # Fallback to substring match
        target = next((s for s in all_states if state_name.lower().strip() in s["state"].lower()), all_states[0])

    # Find blackspots in this state
    db_spots = db.query(Accident).filter(func.lower(Accident.state) == target["state"].lower()).all()
    spot_list = []
    for b in db_spots:
        spot_list.append({
            "name": b.location,
            "corridor": b.corridor,
            "district": b.district,
            "risk_score": b.risk_score,
            "fatalities": b.fatalities,
            "dominant_cause": b.dominant_cause,
            "speed_limit": b.speed_limit,
            "observed_speed": b.observed_speed
        })

    # Generate data-driven engineering recommendations
    recs = []
    sev = target.get("severity_2023", 0.0)
    vru = target.get("vulnerable_user_pct", 60.0)
    cause = target.get("top_cause", "Overspeeding")
    
    if sev > 40.0:
        recs.append({
            "tier": "Tier-1 Critical",
            "type": "Emergency Golden Hour Response",
            "action": "Deploy ALS Ambulances every 35km along " + target.get("primary_corridor", "Highways") + " & upgrade district hospital to Level-2 Trauma Center."
        })
    if vru > 60.0:
        recs.append({
            "tier": "Tier-1 High Priority",
            "type": "Vulnerable Road User Safety",
            "action": "Mandate continuous physical barrier/curb-separated 2-wheeler service lanes and grade-separated pedestrian skywalks at urban fringe interchanges."
        })
    recs.append({
        "tier": "Tier-2 Operational",
        "type": "Speed & Hazard Management",
        "action": f"Install solar-powered radar speed displays and AI-powered ANPR cameras to target prevailing issue: {cause}."
    })
    recs.append({
        "tier": "Tier-3 Road Geometry",
        "type": "Geometric Calibration",
        "action": "Super-elevation recalibration, retro-reflective chevron signage, and crash attenuators at high-risk blackspots."
    })

    return {
        "state": target["state"],
        "code": target.get("code", "IN"),
        "zone": target.get("zone", "National"),
        "capital": target.get("capital", ""),
        "national_rank": target.get("national_rank", 1),
        "lat": target.get("lat", 20.5937),
        "lng": target.get("lng", 78.9629),
        "accidents_2023": target.get("accidents_2023", 0),
        "fatalities_2023": target.get("fatalities_2023", 0),
        "injuries_2023": target.get("injuries_2023", 0),
        "severity_2023": target.get("severity_2023", 0.0),
        "top_cause": cause,
        "primary_corridor": target.get("primary_corridor", "National Highway"),
        "vulnerable_user_pct": vru,
        "history": target.get("history", []),
        "blackspots_identified": len(spot_list),
        "blackspots": spot_list[:10],
        "recommendations": recs
    }

def get_50year_historical_trends() -> Dict[str, Any]:
    """Returns MoRTH 50-year historical road safety and motorization trends (1970-2019)."""
    data_path = os.path.join(DATA_DIR, "morth_50year_historical_trends.json")
    if os.path.isfile(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": []}

def get_junction_control_analysis(city: Optional[str] = None) -> Dict[str, Any]:
    """Returns junction control safety distribution across 50 million-plus Indian cities."""
    data_path = os.path.join(DATA_DIR, "million_plus_cities_junction_traffic_control.json")
    if not os.path.isfile(data_path):
        return {"cities": []}
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if city:
        city_lower = city.strip().lower()
        matched = next((c for c in data.get("cities", []) if c["city"].lower() == city_lower or city_lower in c["city"].lower()), None)
        if matched:
            return {
                "title": f"Junction Safety Profile — {matched['city']}",
                "city_data": matched,
                "national_summary": data.get("national_summary"),
                "engineering_implication": data.get("engineering_implication")
            }
    return data

def get_police_blackspots_registry(state: Optional[str] = None, query: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
    """Returns MoRTH official police station blackspots registry (2016-2018 records)."""
    data_path = os.path.join(DATA_DIR, "official_police_blackspots_registry.json")
    if not os.path.isfile(data_path):
        return {"spots": []}
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    spots = data.get("spots", [])
    if state and state.strip() and state.lower() != "all":
        st_lower = state.strip().lower()
        spots = [s for s in spots if s.get("state", "").lower() == st_lower or st_lower in s.get("state", "").lower()]
    if query and query.strip():
        q_lower = query.strip().lower()
        spots = [s for s in spots if (
            q_lower in s.get("location", "").lower() or
            q_lower in s.get("police_station", "").lower() or
            q_lower in s.get("district", "").lower() or
            q_lower in s.get("highway", "").lower() or
            q_lower in s.get("state", "").lower()
        )]
    return {
        "title": data.get("title"),
        "total_matched": len(spots),
        "total_blackspots_in_registry": data.get("total_blackspots", len(data.get("spots", []))),
        "states_covered": data.get("states_covered", []),
        "spots": spots[:limit]
    }

def get_highways_network(risk_level: Optional[str] = None, state: Optional[str] = None) -> Dict[str, Any]:
    """Returns color-coded Indian highway risk network (Green=Safe, Yellow=Low, Orange=Moderate, Red=Extreme)."""
    data_path = os.path.join(DATA_DIR, "indian_highways_risk_network.json")
    if not os.path.isfile(data_path):
        return {"highways": []}
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    highways = data.get("highways", [])
    if risk_level and risk_level.strip().lower() != "all":
        rl_lower = risk_level.strip().lower()
        highways = [h for h in highways if h.get("risk_level", "").lower() == rl_lower or h.get("color", "").lower() == rl_lower]
    if state and state.strip().lower() != "all":
        st_lower = state.strip().lower()
        highways = [h for h in highways if st_lower in h.get("state", "").lower()]
    return {
        "title": data.get("title"),
        "color_legend": data.get("color_legend"),
        "total_highways": len(highways),
        "total_audited_km": sum(h.get("length_km", 0) for h in highways),
        "highways": highways
    }
