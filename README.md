# 🛡️ RoadSafe India — AI Road Safety Intelligence Platform
> **Problem Statement No. 3 — Transport: RoadSafe India**  
> **National Level Hackathon | Team 015**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Leaflet GIS](https://img.shields.io/badge/GIS%20Mapping-Leaflet.js-199900.svg?logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📌 Executive Summary

India accounts for approximately **11% of global road crash fatalities** despite possessing only **1% of the world's vehicle population**. Official open government data from the **Ministry of Road Transport & Highways (MoRTH)** and the **National Crime Records Bureau (NCRB ADSI 2023)** reveals that over **1,68,000 lives are lost annually** on Indian roads.

**RoadSafe India** is an AI-powered Decision Support Cockpit built for transport ministries, district collectors, traffic police, and highway infrastructure planners. Rather than merely visualizing past accidents, RoadSafe India transforms heterogeneous historical and spatial open government datasets into **actionable, predictive intelligence** to prevent crashes before they occur.

---

## 🎯 Direct Alignment with Problem Statement Questions

| # | Problem Statement Challenge | RoadSafe India Solution & AI Capability |
|---|---|---|
| **1** | **Where are accidents most likely to occur?** | **Interactive GIS Risk Map & Blackspot Cluster Engine**: Ranks **130 geocoded Indian Blackspots & hazard zones** across all 36 States & Union Territories across all three severity tiers (**🔴 Critical $\ge 80$: 41 spots**, **🟠 High $60-79$: 55 spots**, and **🔵 Moderate $< 60$: 34 spots**) with live interactive filter chips, plus a **50-corridor color-coded major highway network (7,749 km)** categorized into Green (Safe), Yellow (Very Few), Orange (Moderate), and Red (Extreme). |
| **2** | **Why are accidents occurring there?** | **Explainable AI (XAI) & Causal Attribution**: Quantifies exact additive feature weights (e.g., *Overspeeding +28 pts*, *Unlit dusk window +14 pts*, *Wet monsoon surface +10 pts*, *Blind curve geometry +14 pts*). Integrates official MoRTH cause distributions (Overspeeding accounts for 69.6% of crashes). |
| **3** | **Who/what is most vulnerable?** | **Vulnerable Road User (VRU) Profiler**: Mode-of-transport risk analysis revealing that **Two-wheelers (44.5%)** and **Pedestrians (19.5%)** comprise **64% of all road fatalities**, while Heavy Commercial Trucks (HCV) act as primary lethal colliding agents. |
| **4** | **When is the risk highest?** | **24-Hour Diurnal & Seasonal Hazard Matrix**: Pinpoints the critical **18:00 – 21:00 dusk rush** (twilight glare + peak commuter density) and **21:00 – 03:00 freight speed window**, alongside seasonal **Monsoon hydroplaning** (June–Sept) and **Winter radiation fog** (Dec–Feb). |
| **5** | **What intervention should be implemented first?** | **Ranked IRC-Standard Engineering & Enforcement**: Prioritizes Indian Roads Congress (IRC) interventions: P1 Immediate (Speed Radars under *IRC:SP:108*, Pedestrian Islands under *IRC:103*, High-Mast Lighting under *IRC:SP:73*, Golden Hour EMS); P2 High (Anti-skid micro-surfacing under *IRC:SP:81*, Curve realignments under *IRC:73*). |
| **6** | **Can we predict whether the intervention will reduce accidents?** | **Interactive Counterfactual "What-If" Simulator**: Quantifies combined safety benefits using empirical crash modification factors (CMF) with diminishing returns: outputs new simulated risk score (e.g. 84 $\rightarrow$ 29), crash reduction %, annual lives saved counter, and safety ROI rating. |

---

## 📊 Dataset Stack Integrated

The platform bundles authentic, standardized datasets based on official government reports:

1. **Dataset A — Pan-India MoRTH State/UT Time-Series (2018–2023)** (`data/morth_timeseries_state_accidents.json`): Complete dataset covering **all 36 Indian States & Union Territories** (28 States + 8 UTs) with longitudinal accident, fatality, injury, severity %, and primary corridor statistics.
2. **Dataset B & C — NCRB ADSI 2023 & MoRTH Detailed Reports**: City-level and national highway casualty counts.
3. **Dataset D — Cause of Accident Classifications** (`data/causes_distribution.json`): Official cause breakdown (Overspeeding 69.6%, Wrong side driving 5.8%, Substandard geometry 5.2%, Adverse weather 4.3%, Potholes/defects 4.2%, Drunk driving 3.5%, etc.).
4. **Dataset E — Mode of Transport & VRU Exposure** (`data/transport_modes_vulnerability.json`): Fatality distribution across Two-wheelers, Pedestrians, Cars/SUVs, Trucks, Auto-rickshaws, Buses, Bicycles.
5. **Diurnal 24-Hour & Seasonality Grid** (`data/diurnal_temporal_distribution.json`): Hourly casualty shares and seasonal multipliers.
6. **National Blackspots & Hazard Database (130 Geocoded Locations across 3 Tiers)** (`data/indian_blackspots_database.json`): 130 geocoded accident clusters across all 36 States & UTs with coordinates, AADT, speed limits, lighting, geometry, calibrated ML risk scores, and full distribution across **Critical (41)**, **High (55)**, and **Moderate (34)**.
7. **Golden Hour Emergency Trauma Centers** (`data/trauma_care_centers.json`): Network of 22 Level-1 and Level-2 Trauma Care hospitals and ambulance dispatch stations nationwide.
8. **MoRTH 50-Year Historical Motorization & Safety Trends (1970–2019)** (`data/morth_50year_historical_trends.json`): Longitudinal dataset of registered motor vehicles (+21,112%), fatalities (+942%), road network length, and population/vehicle normalized fatality rates.
9. **MoRTH Official Police Station Blackspot Registry (2016–2018)** (`data/official_police_blackspots_registry.json`): 270+ audited blackspots across 30 states with exact police stations, highway numbers, chainages, and 3-year casualty histories.
10. **Intersection Traffic Control Matrix across 50 Million-Plus Cities** (`data/million_plus_cities_junction_traffic_control.json`): Casualty distribution across Traffic Light Signals, Police Controlled, Stop Signs, Flashing Blinkers, and Uncontrolled Junctions.
11. **Color-Coded Pan-India Major Highway Risk Network (50 Corridors, 7,749 km)** (`data/indian_highways_risk_network.json`): Comprehensive GIS polyline network color-coded by accident frequency: 🟢 Green (Safe / 0 Fatalities), 🟡 Yellow (Very Few / 1–15 Crashes), 🟠 Orange (Moderate / 16–44 Crashes), and 🔴 Red (Extreme / 45+ Crashes).


---

## 🧠 AI & Machine Learning Architecture

```
                               ┌──────────────────────────────────────────────────────────┐
                               │                 RoadSafe India AI Engine                 │
                               └──────────────────────────────────────────────────────────┘
                                                             │
                  ┌───────────────────────────┬──────────────┴───────────────┬────────────────────────────┐
                  ▼                           ▼                              ▼                            ▼
      ┌───────────────────────┐   ┌──────────────────────────┐   ┌────────────────────────┐   ┌───────────────────────────┐
      │  Calibrated ML Risk   │   │     Explainable AI       │   │  Predictive Forecast   │   │ Counterfactual Simulator  │
      │    Scoring (0-100)    │   │  (Feature Attribution)   │   │ (30/60/90-Day Horizon) │   │ (What-If Intervention)    │
      ├───────────────────────┤   ├──────────────────────────┤   ├────────────────────────┤   ├───────────────────────────┤
      │ • Speed Differential  │   │ • Additive weight score  │   │ • Seasonal Multipliers │   │ • Diminishing returns CMF │
      │ • Surface Friction    │   │ • Specific risk driver   │   │ • Monsoon Hydroplaning │   │ • New simulated risk      │
      │ • Geometry Hazard     │   │ • Actionable IRC advice  │   │ • Winter Fog Index     │   │ • Annual lives saved      │
      │ • Diurnal Exposure    │   │ • Safe operating speed   │   │ • 95% Confidence Band  │   │ • Safety ROI Rating       │
      └───────────────────────┘   └──────────────────────────┘   └────────────────────────┘   └───────────────────────────┘
```

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.10+ (Python 3.13 supported)
- Modern web browser (Chrome, Edge, Firefox)

### Step 1: Clone the Repository
```bash
git clone https://github.com/nandeshmontfort-bot/Team_015.git
cd Team_015
```

### Step 2: One-Click Startup on Windows
Double-click `run_windows.bat` or run from PowerShell / CMD:
```bat
run_windows.bat
```

### Manual Installation (Linux / macOS / Windows)
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt

# 2. Run automated test suite
python tests/test_api.py

# 3. Start Uvicorn ASGI Server
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser at:
- 🌐 **Command Center Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📚 **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 📖 **ReDoc OpenAPI Specifications**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔌 API Endpoint Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Service health status check |
| `GET` | `/api/v1/meta` | Hackathon metadata & problem statement answer mapping |
| `GET` | `/api/v1/accidents/stats/summary` | National & state-filtered KPI statistics |
| `GET` | `/api/v1/accidents/analytics/hotspots` | **Q1**: Ranked geocoded blackspots with 0-100 risk score and XAI drivers |
| `GET` | `/api/v1/accidents/analytics/risk` | **Q2**: Calculate explainable ML risk score for any coordinate & condition |
| `POST` | `/api/v1/accidents/analytics/predict-segment` | **Q2**: JSON-based road segment risk auditor |
| `GET` | `/api/v1/accidents/analytics/causes` | **Q2**: MoRTH cause distribution dataset & analytical takeaways |
| `GET` | `/api/v1/accidents/analytics/vulnerability` | **Q3**: Mode of transport & Vulnerable Road User (VRU) profile |
| `GET` | `/api/v1/accidents/analytics/temporal` | **Q4**: 24-hour diurnal risk curve and seasonal monsoon/fog indices |
| `GET` | `/api/v1/accidents/analytics/prediction` | **Q4**: 30, 60, 90-day time-series risk forecasting with confidence bounds |
| `GET` | `/api/v1/accidents/analytics/interventions` | **Q5**: Ranked IRC-standard engineering & enforcement interventions |
| `POST` | `/api/v1/accidents/analytics/simulate` | **Q6**: Interactive Counterfactual "What-If" impact simulation engine |
| `GET` | `/api/v1/accidents/analytics/states` | Pan-India ranking & metrics for all 36 States & Union Territories |
| `GET` | `/api/v1/accidents/analytics/states/{state_name}` | In-depth State Road Safety Dossier & IRC engineering action plan |
| `GET` | `/api/v1/accidents/analytics/historical-50yr` | MoRTH 50-Year (1970–2019) longitudinal motorization & safety trends |
| `GET` | `/api/v1/accidents/analytics/junction-control` | 50 Million-Plus Cities intersection traffic control crash distribution |
| `GET` | `/api/v1/accidents/analytics/police-blackspots` | MoRTH 270+ audited police station blackspots registry (2016–2018) |
| `GET` | `/api/v1/accidents/analytics/route-risk` | Safe routing & corridor hazard assessment between two cities |
| `GET` | `/api/v1/accidents/analytics/trauma-centers` | Golden Hour emergency trauma care hospital locator |
| `POST` | `/api/v1/accidents/seed-demo` | Seeds authentic Indian blackspots into intelligence base |
| `POST` | `/api/v1/accidents/import-csv` | Bulk imports accident records via CSV upload |
| `POST` | `/api/v1/accidents/` | Register new incident or reported road hazard |
| `GET` | `/api/v1/accidents/{id}` | Retrieve individual incident record |
| `DELETE` | `/api/v1/accidents/{id}` | Delete incident record |

---

## 🧪 Verification & Automated Testing

A comprehensive automated test suite is included in `tests/test_api.py` validating all 6 questions of Problem Statement 3, data integrity, and REST endpoints:

```bash
python tests/test_api.py
```

**Test Execution Results:**
```text
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.729s

OK
```


---

## 🏛️ Decision Support Cockpit Modules

1. **National Command Center**: Live KPIs, GIS Leaflet map with pulsing critical markers (>80 score), and instantaneous Explainable AI inspector.
2. **Where & Why (Spatial & Causal Intelligence)**: All 36 State & UT rankings, National Highway vs State Highway severity paradox, and MoRTH cause breakdowns.
3. **Who & When (Vulnerability & Temporal Matrix)**: VRU vulnerability indices (Two-wheelers vs Pedestrians vs Heavy Trucks) and 24-hour diurnal hazard curve (18:00–21:00 peak).
4. **50-Year Trends & City Junctions**: 50-year motorization vs fatality visualizer (1970–2019), 50 million-plus cities intersection traffic control matrix (Uncontrolled vs Signals), and 270+ audited police station blackspots registry.
5. **AI Risk Predictor & Segment Auditor**: Interactive feature simulator with 0–100 calibrated scoring and 30/60/90-day forecasting with 95% confidence intervals.
6. **Counterfactual Intervention Simulator**: Interactive policy sandbox predicting crash reduction %, lives saved/year, and IRC safety ROI for selected interventions.
7. **Safe Route & Golden Hour Dispatch**: Evaluates corridor hazard between cities (e.g., Delhi–Agra, Mumbai–Pune) and maps nearest Level-1 trauma care centers.
8. **Accident Evidence Base**: Searchable data table, CSV import, sample download, and new incident registration.

---

