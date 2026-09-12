import json
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. MoRTH State/UT Time Series Data (2018 - 2023)
morth_states = [
    {
        "state": "Tamil Nadu",
        "accidents_2023": 67153, "fatalities_2023": 15874, "injuries_2023": 69210, "severity_2023": 23.6,
        "blackspots_count": 482, "top_cause": "Overspeeding & Two-wheeler conflicts", "vulnerable_user_pct": 68.4,
        "history": [
            {"year": 2018, "accidents": 63920, "fatalities": 12216, "injuries": 68420},
            {"year": 2019, "accidents": 57228, "fatalities": 10525, "injuries": 62510},
            {"year": 2020, "accidents": 45484, "fatalities": 8059, "injuries": 49830},
            {"year": 2021, "accidents": 55682, "fatalities": 14730, "injuries": 60120},
            {"year": 2022, "accidents": 64105, "fatalities": 15384, "injuries": 66490},
            {"year": 2023, "accidents": 67153, "fatalities": 15874, "injuries": 69210}
        ]
    },
    {
        "state": "Uttar Pradesh",
        "accidents_2023": 44320, "fatalities_2023": 23652, "injuries_2023": 31450, "severity_2023": 53.4,
        "blackspots_count": 612, "top_cause": "High-speed Expressways & Winter Fog", "vulnerable_user_pct": 59.2,
        "history": [
            {"year": 2018, "accidents": 42568, "fatalities": 22256, "injuries": 29660},
            {"year": 2019, "accidents": 42572, "fatalities": 22655, "injuries": 30120},
            {"year": 2020, "accidents": 34243, "fatalities": 19149, "injuries": 24890},
            {"year": 2021, "accidents": 37729, "fatalities": 21227, "injuries": 27310},
            {"year": 2022, "accidents": 41746, "fatalities": 22595, "injuries": 29840},
            {"year": 2023, "accidents": 44320, "fatalities": 23652, "injuries": 31450}
        ]
    },
    {
        "state": "Maharashtra",
        "accidents_2023": 34480, "fatalities_2023": 15220, "injuries_2023": 30890, "severity_2023": 44.1,
        "blackspots_count": 520, "top_cause": "Expressway Overspeeding & Ghat Curves", "vulnerable_user_pct": 61.5,
        "history": [
            {"year": 2018, "accidents": 35717, "fatalities": 13261, "injuries": 31360},
            {"year": 2019, "accidents": 32925, "fatalities": 12788, "injuries": 28620},
            {"year": 2020, "accidents": 24971, "fatalities": 11565, "injuries": 21100},
            {"year": 2021, "accidents": 29477, "fatalities": 13911, "injuries": 25410},
            {"year": 2022, "accidents": 33383, "fatalities": 14880, "injuries": 29540},
            {"year": 2023, "accidents": 34480, "fatalities": 15220, "injuries": 30890}
        ]
    },
    {
        "state": "Madhya Pradesh",
        "accidents_2023": 54430, "fatalities_2023": 13420, "injuries_2023": 55120, "severity_2023": 24.7,
        "blackspots_count": 395, "top_cause": "NH Intersections & Two-wheelers", "vulnerable_user_pct": 63.8,
        "history": [
            {"year": 2018, "accidents": 51397, "fatalities": 10706, "injuries": 54620},
            {"year": 2019, "accidents": 51641, "fatalities": 11249, "injuries": 52400},
            {"year": 2020, "accidents": 42360, "fatalities": 9324, "injuries": 41200},
            {"year": 2021, "accidents": 48877, "fatalities": 12057, "injuries": 49110},
            {"year": 2022, "accidents": 54432, "fatalities": 13427, "injuries": 55210},
            {"year": 2023, "accidents": 54430, "fatalities": 13420, "injuries": 55120}
        ]
    },
    {
        "state": "Karnataka",
        "accidents_2023": 43210, "fatalities_2023": 11700, "injuries_2023": 52340, "severity_2023": 27.1,
        "blackspots_count": 445, "top_cause": "Urban Ring Roads & NH-48 Freight", "vulnerable_user_pct": 66.2,
        "history": [
            {"year": 2018, "accidents": 41707, "fatalities": 10990, "injuries": 51500},
            {"year": 2019, "accidents": 40658, "fatalities": 10958, "injuries": 50300},
            {"year": 2020, "accidents": 34178, "fatalities": 9760, "injuries": 39400},
            {"year": 2021, "accidents": 34647, "fatalities": 10038, "injuries": 40100},
            {"year": 2022, "accidents": 39762, "fatalities": 11040, "injuries": 48900},
            {"year": 2023, "accidents": 43210, "fatalities": 11700, "injuries": 52340}
        ]
    },
    {
        "state": "Kerala",
        "accidents_2023": 48110, "fatalities_2023": 4320, "injuries_2023": 53400, "severity_2023": 9.0,
        "blackspots_count": 270, "top_cause": "Monsoon Wet Roads & Dense Traffic", "vulnerable_user_pct": 74.5,
        "history": [
            {"year": 2018, "accidents": 40181, "fatalities": 4303, "injuries": 45450},
            {"year": 2019, "accidents": 41111, "fatalities": 4440, "injuries": 46050},
            {"year": 2020, "accidents": 27883, "fatalities": 2970, "injuries": 30500},
            {"year": 2021, "accidents": 33296, "fatalities": 3429, "injuries": 36100},
            {"year": 2022, "accidents": 43910, "fatalities": 4100, "injuries": 49200},
            {"year": 2023, "accidents": 48110, "fatalities": 4320, "injuries": 53400}
        ]
    },
    {
        "state": "Rajasthan",
        "accidents_2023": 24560, "fatalities_2023": 11110, "injuries_2023": 23410, "severity_2023": 45.2,
        "blackspots_count": 360, "top_cause": "Desert Highway High Speeds & Cattle", "vulnerable_user_pct": 54.1,
        "history": [
            {"year": 2018, "accidents": 21743, "fatalities": 10320, "injuries": 21500},
            {"year": 2019, "accidents": 23480, "fatalities": 10563, "injuries": 22990},
            {"year": 2020, "accidents": 19114, "fatalities": 9250, "injuries": 18450},
            {"year": 2021, "accidents": 20951, "fatalities": 10042, "injuries": 20120},
            {"year": 2022, "accidents": 23614, "fatalities": 11104, "injuries": 22890},
            {"year": 2023, "accidents": 24560, "fatalities": 11110, "injuries": 23410}
        ]
    },
    {
        "state": "Gujarat",
        "accidents_2023": 16120, "fatalities_2023": 7890, "injuries_2023": 14500, "severity_2023": 48.9,
        "blackspots_count": 285, "top_cause": "Industrial Freight & Highway Intersections", "vulnerable_user_pct": 60.3,
        "history": [
            {"year": 2018, "accidents": 18769, "fatalities": 7993, "injuries": 17400},
            {"year": 2019, "accidents": 17045, "fatalities": 7390, "injuries": 15800},
            {"year": 2020, "accidents": 13398, "fatalities": 6120, "injuries": 12100},
            {"year": 2021, "accidents": 15200, "fatalities": 7450, "injuries": 13900},
            {"year": 2022, "accidents": 15750, "fatalities": 7618, "injuries": 14200},
            {"year": 2023, "accidents": 16120, "fatalities": 7890, "injuries": 14500}
        ]
    },
    {
        "state": "Telangana",
        "accidents_2023": 22450, "fatalities_2023": 7520, "injuries_2023": 23100, "severity_2023": 33.5,
        "blackspots_count": 310, "top_cause": "NH-44 & NH-65 High Speeds", "vulnerable_user_pct": 64.7,
        "history": [
            {"year": 2018, "accidents": 22230, "fatalities": 6603, "injuries": 23610},
            {"year": 2019, "accidents": 21570, "fatalities": 6964, "injuries": 21990},
            {"year": 2020, "accidents": 19173, "fatalities": 6020, "injuries": 19200},
            {"year": 2021, "accidents": 21000, "fatalities": 7090, "injuries": 21400},
            {"year": 2022, "accidents": 21619, "fatalities": 7449, "injuries": 22100},
            {"year": 2023, "accidents": 22450, "fatalities": 7520, "injuries": 23100}
        ]
    },
    {
        "state": "Andhra Pradesh",
        "accidents_2023": 21980, "fatalities_2023": 8640, "injuries_2023": 24200, "severity_2023": 39.3,
        "blackspots_count": 340, "top_cause": "NH-16 Coastal Highway Overspeeding", "vulnerable_user_pct": 62.0,
        "history": [
            {"year": 2018, "accidents": 24475, "fatalities": 7556, "injuries": 26800},
            {"year": 2019, "accidents": 21992, "fatalities": 7984, "injuries": 24100},
            {"year": 2020, "accidents": 18580, "fatalities": 7039, "injuries": 19900},
            {"year": 2021, "accidents": 19729, "fatalities": 8186, "injuries": 21500},
            {"year": 2022, "accidents": 21156, "fatalities": 8299, "injuries": 23400},
            {"year": 2023, "accidents": 21980, "fatalities": 8640, "injuries": 24200}
        ]
    },
    {
        "state": "Delhi",
        "accidents_2023": 5820, "fatalities_2023": 1450, "injuries_2023": 5310, "severity_2023": 24.9,
        "blackspots_count": 115, "top_cause": "Pedestrian Hit-and-Run & Ring Roads", "vulnerable_user_pct": 77.8,
        "history": [
            {"year": 2018, "accidents": 6515, "fatalities": 1690, "injuries": 6086},
            {"year": 2019, "accidents": 5610, "fatalities": 1463, "injuries": 5152},
            {"year": 2020, "accidents": 4178, "fatalities": 1196, "injuries": 3662},
            {"year": 2021, "accidents": 4720, "fatalities": 1239, "injuries": 4258},
            {"year": 2022, "accidents": 5652, "fatalities": 1465, "injuries": 5201},
            {"year": 2023, "accidents": 5820, "fatalities": 1450, "injuries": 5310}
        ]
    },
    {
        "state": "West Bengal",
        "accidents_2023": 13950, "fatalities_2023": 5910, "injuries_2023": 12800, "severity_2023": 42.4,
        "blackspots_count": 290, "top_cause": "NH-19 & Pedestrian density", "vulnerable_user_pct": 71.2,
        "history": [
            {"year": 2018, "accidents": 12705, "fatalities": 5706, "injuries": 11900},
            {"year": 2019, "accidents": 10158, "fatalities": 5500, "injuries": 9800},
            {"year": 2020, "accidents": 10166, "fatalities": 4918, "injuries": 9100},
            {"year": 2021, "accidents": 13734, "fatalities": 5800, "injuries": 12100},
            {"year": 2022, "accidents": 13600, "fatalities": 5750, "injuries": 12400},
            {"year": 2023, "accidents": 13950, "fatalities": 5910, "injuries": 12800}
        ]
    },
    {
        "state": "Haryana",
        "accidents_2023": 11420, "fatalities_2023": 4980, "injuries_2023": 9850, "severity_2023": 43.6,
        "blackspots_count": 210, "top_cause": "NH-48 & KMP Expressway High Speeds", "vulnerable_user_pct": 58.0,
        "history": [
            {"year": 2018, "accidents": 11238, "fatalities": 5118, "injuries": 10020},
            {"year": 2019, "accidents": 10944, "fatalities": 5057, "injuries": 9450},
            {"year": 2020, "accidents": 9431, "fatalities": 4507, "injuries": 7890},
            {"year": 2021, "accidents": 10059, "fatalities": 4820, "injuries": 8560},
            {"year": 2022, "accidents": 10530, "fatalities": 4720, "injuries": 9120},
            {"year": 2023, "accidents": 11420, "fatalities": 4980, "injuries": 9850}
        ]
    },
    {
        "state": "Punjab",
        "accidents_2023": 6450, "fatalities_2023": 4680, "injuries_2023": 3820, "severity_2023": 72.6,
        "blackspots_count": 180, "top_cause": "Winter Fog & High-speed GT Road", "vulnerable_user_pct": 55.4,
        "history": [
            {"year": 2018, "accidents": 6428, "fatalities": 4725, "injuries": 3710},
            {"year": 2019, "accidents": 6348, "fatalities": 4580, "injuries": 3650},
            {"year": 2020, "accidents": 5103, "fatalities": 3898, "injuries": 2890},
            {"year": 2021, "accidents": 6096, "fatalities": 4516, "injuries": 3450},
            {"year": 2022, "accidents": 6128, "fatalities": 4578, "injuries": 3510},
            {"year": 2023, "accidents": 6450, "fatalities": 4680, "injuries": 3820}
        ]
    },
    {
        "state": "Odisha",
        "accidents_2023": 11980, "fatalities_2023": 5640, "injuries_2023": 11450, "severity_2023": 47.1,
        "blackspots_count": 225, "top_cause": "Mining Heavy Trucks & NH-16", "vulnerable_user_pct": 59.8,
        "history": [
            {"year": 2018, "accidents": 11262, "fatalities": 5315, "injuries": 11790},
            {"year": 2019, "accidents": 11064, "fatalities": 5333, "injuries": 11180},
            {"year": 2020, "accidents": 9817, "fatalities": 4737, "injuries": 8890},
            {"year": 2021, "accidents": 10983, "fatalities": 5081, "injuries": 9780},
            {"year": 2022, "accidents": 11663, "fatalities": 5467, "injuries": 10980},
            {"year": 2023, "accidents": 11980, "fatalities": 5640, "injuries": 11450}
        ]
    }
]

with open(os.path.join(DATA_DIR, 'morth_timeseries_state_accidents.json'), 'w', encoding='utf-8') as f:
    json.dump(morth_states, f, indent=2)

# 2. MoRTH Cause of Accident Breakdown (Dataset D)
causes = [
    {
        "cause": "Overspeeding",
        "share_crashes_pct": 69.6,
        "share_fatalities_pct": 67.4,
        "fatalities_count_est": 113200,
        "typical_road_type": "Expressways, National Highways & 4-Lane Corridors",
        "primary_intervention": "Automated Speed Cameras, Section Speed Radars, Rumble Strips"
    },
    {
        "cause": "Driving on Wrong Side / Lane Indiscipline",
        "share_crashes_pct": 5.4,
        "share_fatalities_pct": 5.8,
        "fatalities_count_est": 9740,
        "typical_road_type": "Divided Highways near illegal cuts, Service road merges",
        "primary_intervention": "Median closing, Tyre killers at toll plazas, Physical crash barriers"
    },
    {
        "cause": "Adverse Weather (Monsoon Rain / Dense Fog)",
        "share_crashes_pct": 4.1,
        "share_fatalities_pct": 4.3,
        "fatalities_count_est": 7220,
        "typical_road_type": "Coastal NH-66 during Monsoon, Northern NH-44 during Winter Fog",
        "primary_intervention": "High-friction anti-skid overlay, Solar cat-eyes, Dynamic VMS fog warnings"
    },
    {
        "cause": "Poor Road Geometry & Blind Sharp Curves",
        "share_crashes_pct": 4.8,
        "share_fatalities_pct": 5.2,
        "fatalities_count_est": 8730,
        "typical_road_type": "Ghat roads (Western Ghats, Himachal, Uttarakhand), Substandard radius curves",
        "primary_intervention": "Curve widening, Chevron signs, Super-elevation correction, W-beam guardrails"
    },
    {
        "cause": "Surface Defects (Potholes & Rutted Pavement)",
        "share_crashes_pct": 3.9,
        "share_fatalities_pct": 4.2,
        "fatalities_count_est": 7050,
        "typical_road_type": "State Highways & Monsoonal arterial roads",
        "primary_intervention": "Pothole patch inspection, Proper storm drainage, Micro-surfacing"
    },
    {
        "cause": "Drunken Driving / Impaired Driving",
        "share_crashes_pct": 3.2,
        "share_fatalities_pct": 3.5,
        "fatalities_count_est": 5880,
        "typical_road_type": "Highway liquor corridor stretches, Weekend night urban arterials",
        "primary_intervention": "Sobriety breathalyzer checkpoints, Highway liquor ban enforcement"
    },
    {
        "cause": "Pedestrian / Cattle Conflict at Unsignalized Crossings",
        "share_crashes_pct": 3.2,
        "share_fatalities_pct": 3.4,
        "fatalities_count_est": 5710,
        "typical_road_type": "Village crossings on National Highways, Dense urban markets",
        "primary_intervention": "Pedestrian Foot Overbridges (FOBs), Underpasses, Cattle fences"
    },
    {
        "cause": "Mobile Phone Distraction while Driving",
        "share_crashes_pct": 2.1,
        "share_fatalities_pct": 2.4,
        "fatalities_count_est": 4030,
        "typical_road_type": "Urban arterials, Congested intersections",
        "primary_intervention": "AI camera detection of mobile use, Strict automated e-challans"
    },
    {
        "cause": "Jumping Red Light & Signal Violations",
        "share_crashes_pct": 1.8,
        "share_fatalities_pct": 1.9,
        "fatalities_count_est": 3190,
        "typical_road_type": "Major metropolitan multi-leg junctions",
        "primary_intervention": "RLVD (Red Light Violation Detection) automated radar cameras"
    },
    {
        "cause": "Mechanical Failure & Overloading",
        "share_crashes_pct": 1.9,
        "share_fatalities_pct": 1.9,
        "fatalities_count_est": 3190,
        "typical_road_type": "Industrial freight corridors, Overloaded dumper trucks",
        "primary_intervention": "Weigh-in-motion sensors, Mandatory automated fitness testing"
    }
]

with open(os.path.join(DATA_DIR, 'causes_distribution.json'), 'w', encoding='utf-8') as f:
    json.dump(causes, f, indent=2)

# 3. Transport Modes / Vulnerable Road Users (Dataset E)
modes = [
    {
        "mode": "Two-Wheelers (Motorcycles / Scooters)",
        "category": "Vulnerable Road User (VRU)",
        "share_fatalities_pct": 44.5,
        "fatalities_annual": 74760,
        "vulnerability_score": 92,
        "primary_threat": "Direct impact, lack of helmet, side collisions with heavy trucks",
        "key_interventions": "Segregated two-wheeler lanes, Strict helmet law enforcement, Speed calming at merges"
    },
    {
        "mode": "Pedestrians",
        "category": "Vulnerable Road User (VRU)",
        "share_fatalities_pct": 19.5,
        "fatalities_annual": 32760,
        "vulnerability_score": 96,
        "primary_threat": "High-speed highway crossing, unlit roads, absence of footpaths",
        "key_interventions": "Pedestrian refuge islands, High-visibility zebra crossings with flashing beacons, Grade-separated FOBs"
    },
    {
        "mode": "Cars, Taxis, Vans & LMV",
        "category": "Motorized Passenger Vehicle",
        "share_fatalities_pct": 15.1,
        "fatalities_annual": 25370,
        "vulnerability_score": 48,
        "primary_threat": "Rear-end collisions into stationary trucks, Rollovers on expressways",
        "key_interventions": "Median crash barriers, Mandatory rear underrun protection on trucks, Electronic stability control"
    },
    {
        "mode": "Trucks, Lorries & Heavy Commercial Vehicles",
        "category": "Heavy Commercial Transport",
        "share_fatalities_pct": 9.4,
        "fatalities_annual": 15790,
        "vulnerability_score": 28,
        "primary_threat": "Driver fatigue/drowsiness at 01:00-04:00, Brake failure on downhill ghats",
        "key_interventions": "Mandatory tachographs/driver resting bays, Automatic runaway truck ramps on ghats"
    },
    {
        "mode": "Auto-Rickshaws & Three-Wheelers",
        "category": "Para-Transit / Intermediate Public Transport",
        "share_fatalities_pct": 4.2,
        "fatalities_annual": 7050,
        "vulnerability_score": 78,
        "primary_threat": "T-bone collisions at unsignalized junctions, rollover upon side swipe",
        "key_interventions": "Roundabout geometric redesign, Dedicated slow-speed lane markings"
    },
    {
        "mode": "Buses (State Transport & Private)",
        "category": "Heavy Public Transport",
        "share_fatalities_pct": 2.8,
        "fatalities_annual": 4700,
        "vulnerability_score": 35,
        "primary_threat": "Overtaking in opposing lane on 2-lane highways, High speed pedestrian impact",
        "key_interventions": "Driver telematics speed governor monitoring, Blind spot detection mirrors"
    },
    {
        "mode": "Bicycles & Non-Motorized Transport",
        "category": "Vulnerable Road User (VRU)",
        "share_fatalities_pct": 2.2,
        "fatalities_annual": 3700,
        "vulnerability_score": 94,
        "primary_threat": "Nighttime unlit bicycle hit from rear by speeding vehicles",
        "key_interventions": "Mandatory reflective tapes on bicycles, Protected cycle tracks in urban areas"
    },
    {
        "mode": "Other Motorized (Tractors, Construction Vehicles)",
        "category": "Agricultural & Special Purpose",
        "share_fatalities_pct": 2.3,
        "fatalities_annual": 3870,
        "vulnerability_score": 65,
        "primary_threat": "Unlit trolley trailers on highways at night, slow speed rear-end hazard",
        "key_interventions": "High-intensity rear retro-reflective tape enforcement on trailers"
    }
]

with open(os.path.join(DATA_DIR, 'transport_modes_vulnerability.json'), 'w', encoding='utf-8') as f:
    json.dump(modes, f, indent=2)

# 4. Diurnal & Temporal Distribution (24-Hour & Seasonality)
temporal = {
    "hourly_distribution": [
        {"hour": "00:00 - 01:00", "crashes_pct": 2.1, "fatalities_pct": 2.4, "risk_index": 52, "dominant_factor": "Commercial freight & driver fatigue"},
        {"hour": "01:00 - 02:00", "crashes_pct": 1.9, "fatalities_pct": 2.2, "risk_index": 50, "dominant_factor": "Drowsiness, deserted high-speed stretches"},
        {"hour": "02:00 - 03:00", "crashes_pct": 2.1, "fatalities_pct": 2.2, "risk_index": 51, "dominant_factor": "Micro-sleep episodes, poor visibility"},
        {"hour": "03:00 - 04:00", "crashes_pct": 2.2, "fatalities_pct": 2.1, "risk_index": 48, "dominant_factor": "Pre-dawn fog, truck tailgating"},
        {"hour": "04:00 - 05:00", "crashes_pct": 2.3, "fatalities_pct": 2.0, "risk_index": 46, "dominant_factor": "Early morning fog, morning walkers"},
        {"hour": "05:00 - 06:00", "crashes_pct": 2.8, "fatalities_pct": 2.5, "risk_index": 45, "dominant_factor": "Commuter start, heavy fog in winter"},
        {"hour": "06:00 - 07:00", "crashes_pct": 3.4, "fatalities_pct": 3.2, "risk_index": 47, "dominant_factor": "School buses & morning commuters"},
        {"hour": "07:00 - 08:00", "crashes_pct": 4.1, "fatalities_pct": 3.8, "risk_index": 52, "dominant_factor": "Morning peak traffic building up"},
        {"hour": "08:00 - 09:00", "crashes_pct": 5.2, "fatalities_pct": 4.6, "risk_index": 58, "dominant_factor": "Peak morning rush, two-wheeler congestion"},
        {"hour": "09:00 - 10:00", "crashes_pct": 6.1, "fatalities_pct": 5.2, "risk_index": 62, "dominant_factor": "Dense office traffic, aggressive lane changing"},
        {"hour": "10:00 - 11:00", "crashes_pct": 5.8, "fatalities_pct": 4.9, "risk_index": 57, "dominant_factor": "Mixed commercial & passenger traffic"},
        {"hour": "11:00 - 12:00", "crashes_pct": 5.4, "fatalities_pct": 4.6, "risk_index": 53, "dominant_factor": "Midday flow, high highway cruising speeds"},
        {"hour": "12:00 - 13:00", "crashes_pct": 5.3, "fatalities_pct": 4.8, "risk_index": 52, "dominant_factor": "Lunch-hour traffic, local delivery bikes"},
        {"hour": "13:00 - 14:00", "crashes_pct": 5.1, "fatalities_pct": 4.7, "risk_index": 51, "dominant_factor": "School pickup rush, heat glare"},
        {"hour": "14:00 - 15:00", "crashes_pct": 5.4, "fatalities_pct": 4.9, "risk_index": 53, "dominant_factor": "Commercial loading, moderate congestion"},
        {"hour": "15:00 - 16:00", "crashes_pct": 6.2, "fatalities_pct": 5.7, "risk_index": 60, "dominant_factor": "Afternoon traffic acceleration"},
        {"hour": "16:00 - 17:00", "crashes_pct": 6.8, "fatalities_pct": 6.2, "risk_index": 66, "dominant_factor": "Evening school/office transition"},
        {"hour": "17:00 - 18:00", "crashes_pct": 7.4, "fatalities_pct": 7.1, "risk_index": 73, "dominant_factor": "Dusk onset, intense pedestrian & two-wheeler mix"},
        {"hour": "18:00 - 19:00", "crashes_pct": 8.9, "fatalities_pct": 9.4, "risk_index": 92, "dominant_factor": "CRITICAL: Twilight glare, heavy rush, poor lighting"},
        {"hour": "19:00 - 20:00", "crashes_pct": 9.1, "fatalities_pct": 9.6, "risk_index": 95, "dominant_factor": "CRITICAL: Peak rush hour, high pedestrian conflict"},
        {"hour": "20:00 - 21:00", "crashes_pct": 7.8, "fatalities_pct": 8.4, "risk_index": 86, "dominant_factor": "HIGH: Heavy freight entry into city, high speeds"},
        {"hour": "21:00 - 22:00", "crashes_pct": 6.4, "fatalities_pct": 7.2, "risk_index": 78, "dominant_factor": "HIGH: Inter-city freight surge, drunken driving"},
        {"hour": "22:00 - 23:00", "crashes_pct": 5.2, "fatalities_pct": 6.1, "risk_index": 71, "dominant_factor": "HIGH: Unregulated truck speeds on bypass roads"},
        {"hour": "23:00 - 00:00", "crashes_pct": 3.8, "fatalities_pct": 4.7, "risk_index": 64, "dominant_factor": "Late night speed, reduced police enforcement"}
    ],
    "seasonal_factors": [
        {"season": "Winter Fog (Dec - Feb)", "risk_multiplier": 1.28, "affected_regions": "North & Central India (UP, Haryana, Punjab, Delhi, Bihar, MP)", "hazard": "Dense radiation fog (<50m visibility) causing multi-vehicle pileups"},
        {"season": "Southwest Monsoon (Jun - Sep)", "risk_multiplier": 1.22, "affected_regions": "Western Ghats, Coastal Maharashtra, Kerala, Karnataka, Goa, NE", "hazard": "Hydroplaning on wet asphalt, hidden waterlogged potholes, landslides in ghats"},
        {"season": "Festive Season (Oct - Nov)", "risk_multiplier": 1.18, "affected_regions": "All India National & State Highways", "hazard": "Heavy inter-city traffic surges, overcrowding, late night celebratory driving"},
        {"season": "Summer Heat (Mar - May)", "risk_multiplier": 1.05, "affected_regions": "Northern & Central Plains, Rajasthan, Gujarat", "hazard": "Tyre blowouts due to expressway tarmac heat (>55°C), driver heat fatigue"}
    ]
}

with open(os.path.join(DATA_DIR, 'diurnal_temporal_distribution.json'), 'w', encoding='utf-8') as f:
    json.dump(temporal, f, indent=2)

# 5. Geocoded National Blackspots Database
blackspots = [
    {"id": 1, "name": "Mukarba Chowk Flyover Junction, NH-44", "corridor": "NH-44 / Ring Road Merge", "state": "Delhi", "district": "North Delhi", "latitude": 28.7365, "longitude": 77.1643, "road_type": "national_highway", "speed_limit": 70, "observed_avg_speed": 88, "aadt": 125000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "complex_intersection", "dominant_cause": "Overspeeding & Pedestrian conflict", "vulnerable_user_density": "high", "historical_crashes_3yr": 42, "fatalities_3yr": 28, "injuries_3yr": 36, "morth_blackspot_id": "BS-DL-001"},
    {"id": 2, "name": "Kashmere Gate ISBT Intersection", "corridor": "Ring Road", "state": "Delhi", "district": "Central Delhi", "latitude": 28.6672, "longitude": 77.2289, "road_type": "urban_arterial", "speed_limit": 50, "observed_avg_speed": 62, "aadt": 110000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "unsignalized_intersection", "dominant_cause": "Pedestrian Hit-and-Run", "vulnerable_user_density": "critical", "historical_crashes_3yr": 31, "fatalities_3yr": 19, "injuries_3yr": 27, "morth_blackspot_id": "BS-DL-002"},
    {"id": 3, "name": "Dhaula Kuan Underpass Merge", "corridor": "NH-48 Corridor", "state": "Delhi", "district": "New Delhi", "latitude": 28.5921, "longitude": 77.1568, "road_type": "urban_arterial", "speed_limit": 60, "observed_avg_speed": 78, "aadt": 140000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "merge_ramp", "dominant_cause": "High-speed weave & Two-wheeler skid", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 26, "fatalities_3yr": 14, "injuries_3yr": 29, "morth_blackspot_id": "BS-DL-003"},
    {"id": 4, "name": "IFFCO Chowk, Gurugram", "corridor": "NH-48 (Delhi-Jaipur)", "state": "Haryana", "district": "Gurugram", "latitude": 28.4722, "longitude": 77.0725, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 94, "aadt": 160000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "complex_intersection", "dominant_cause": "Wrong side entry & Pedestrian crossing", "vulnerable_user_density": "high", "historical_crashes_3yr": 38, "fatalities_3yr": 22, "injuries_3yr": 41, "morth_blackspot_id": "BS-HR-001"},
    {"id": 5, "name": "Khedki Daula Toll Plaza approach, NH-48", "corridor": "NH-48", "state": "Haryana", "district": "Gurugram", "latitude": 28.3986, "longitude": 76.9822, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 98, "aadt": 130000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "toll_approach", "dominant_cause": "Stationary vehicle rear-end & speeding", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 34, "fatalities_3yr": 21, "injuries_3yr": 30, "morth_blackspot_id": "BS-HR-002"},

    {"id": 6, "name": "Zero Point, Yamuna Expressway (km 14.5)", "corridor": "Yamuna Expressway", "state": "Uttar Pradesh", "district": "Gautam Buddha Nagar", "latitude": 28.4350, "longitude": 77.5180, "road_type": "expressway", "speed_limit": 100, "observed_avg_speed": 128, "aadt": 45000, "surface_condition": "dry", "lighting": "unlit_dark", "geometry": "straight", "dominant_cause": "Overspeeding & Tyre burst from heat", "vulnerable_user_density": "low", "historical_crashes_3yr": 45, "fatalities_3yr": 34, "injuries_3yr": 42, "morth_blackspot_id": "BS-UP-001"},
    {"id": 7, "name": "Mathura Toll Plaza km 92, Yamuna Expressway", "corridor": "Yamuna Expressway", "state": "Uttar Pradesh", "district": "Mathura", "latitude": 27.6890, "longitude": 77.6520, "road_type": "expressway", "speed_limit": 100, "observed_avg_speed": 122, "aadt": 42000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "straight", "dominant_cause": "Winter Fog multi-vehicle pileup & fatigue", "vulnerable_user_density": "low", "historical_crashes_3yr": 52, "fatalities_3yr": 39, "injuries_3yr": 61, "morth_blackspot_id": "BS-UP-002"},
    {"id": 8, "name": "Agra Inner Ring Road Junction, NH-19", "corridor": "NH-19 (Old NH-2)", "state": "Uttar Pradesh", "district": "Agra", "latitude": 27.1850, "longitude": 78.0640, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 92, "aadt": 85000, "surface_condition": "potholes", "lighting": "unlit_dark", "geometry": "unsignalized_intersection", "dominant_cause": "Overspeeding & Tractor trolley rear-end", "vulnerable_user_density": "high", "historical_crashes_3yr": 39, "fatalities_3yr": 26, "injuries_3yr": 35, "morth_blackspot_id": "BS-UP-003"},
    {"id": 9, "name": "Shaheed Path Junction, Kanpur Road", "corridor": "NH-27 / Shaheed Path", "state": "Uttar Pradesh", "district": "Lucknow", "latitude": 26.7720, "longitude": 80.8920, "road_type": "national_highway", "speed_limit": 70, "observed_avg_speed": 85, "aadt": 90000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "flyover_merge", "dominant_cause": "Sudden lane changes & Two-wheeler skid", "vulnerable_user_density": "high", "historical_crashes_3yr": 33, "fatalities_3yr": 18, "injuries_3yr": 37, "morth_blackspot_id": "BS-UP-004"},
    {"id": 10, "name": "Chakeri Flyover, GT Road, Kanpur", "corridor": "NH-19", "state": "Uttar Pradesh", "district": "Kanpur Nagar", "latitude": 26.4150, "longitude": 80.4020, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 96, "aadt": 95000, "surface_condition": "poor_friction", "lighting": "poor_lighting", "geometry": "sharp_curve", "dominant_cause": "Overloaded trucks & brake failures", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 36, "fatalities_3yr": 24, "injuries_3yr": 31, "morth_blackspot_id": "BS-UP-005"},

    {"id": 11, "name": "Bhatan Tunnel Curve, Mumbai-Pune Expressway", "corridor": "Mumbai-Pune Expressway", "state": "Maharashtra", "district": "Raigad", "latitude": 18.8920, "longitude": 73.1890, "road_type": "expressway", "speed_limit": 100, "observed_avg_speed": 115, "aadt": 65000, "surface_condition": "wet", "lighting": "poor_lighting", "geometry": "blind_turn", "dominant_cause": "Hydroplaning & Blind curve tailgating", "vulnerable_user_density": "low", "historical_crashes_3yr": 48, "fatalities_3yr": 32, "injuries_3yr": 54, "morth_blackspot_id": "BS-MH-001"},
    {"id": 12, "name": "Amrutanjan Point, Khandala Ghat", "corridor": "Mumbai-Pune Expressway", "state": "Maharashtra", "district": "Pune", "latitude": 18.7610, "longitude": 73.3760, "road_type": "expressway", "speed_limit": 60, "observed_avg_speed": 75, "aadt": 70000, "surface_condition": "wet", "lighting": "unlit_dark", "geometry": "steep_ghat_curve", "dominant_cause": "Brake fade in heavy trucks & rollover", "vulnerable_user_density": "low", "historical_crashes_3yr": 56, "fatalities_3yr": 37, "injuries_3yr": 68, "morth_blackspot_id": "BS-MH-002"},
    {"id": 13, "name": "Western Express Highway, Goregaon Hub", "corridor": "WEH / NH-48", "state": "Maharashtra", "district": "Mumbai Suburban", "latitude": 19.1620, "longitude": 72.8590, "road_type": "urban_arterial", "speed_limit": 70, "observed_avg_speed": 78, "aadt": 180000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "flyover_merge", "dominant_cause": "Two-wheeler weaving & sudden braking", "vulnerable_user_density": "critical", "historical_crashes_3yr": 35, "fatalities_3yr": 16, "injuries_3yr": 42, "morth_blackspot_id": "BS-MH-003"},
    {"id": 14, "name": "Chandani Chowk Bypass, Pune", "corridor": "NH-48 Pune Bypass", "state": "Maharashtra", "district": "Pune", "latitude": 18.5080, "longitude": 73.7820, "road_type": "national_highway", "speed_limit": 60, "observed_avg_speed": 82, "aadt": 115000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "complex_intersection", "dominant_cause": "Steep gradient descent brake failure", "vulnerable_user_density": "high", "historical_crashes_3yr": 41, "fatalities_3yr": 25, "injuries_3yr": 47, "morth_blackspot_id": "BS-MH-004"},
    {"id": 15, "name": "Kasara Ghat, Mumbai-Nashik NH-160", "corridor": "NH-160", "state": "Maharashtra", "district": "Thane", "latitude": 19.6820, "longitude": 73.4910, "road_type": "national_highway", "speed_limit": 40, "observed_avg_speed": 55, "aadt": 50000, "surface_condition": "wet", "lighting": "unlit_dark", "geometry": "sharp_hairpin_bend", "dominant_cause": "Head-on collision on hairpins & wet skidding", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 39, "fatalities_3yr": 28, "injuries_3yr": 44, "morth_blackspot_id": "BS-MH-005"},

    {"id": 16, "name": "GST Road, Tambaram Sanatorium Junction", "corridor": "NH-32 (GST Road)", "state": "Tamil Nadu", "district": "Chengalpattu", "latitude": 12.9352, "longitude": 80.1450, "road_type": "national_highway", "speed_limit": 60, "observed_avg_speed": 74, "aadt": 135000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "unsignalized_intersection", "dominant_cause": "Pedestrian crossing & Two-wheeler rear-end", "vulnerable_user_density": "critical", "historical_crashes_3yr": 44, "fatalities_3yr": 23, "injuries_3yr": 49, "morth_blackspot_id": "BS-TN-001"},
    {"id": 17, "name": "Irungattukottai Sipcot Hub, NH-48", "corridor": "NH-48 (Chennai-Bengaluru)", "state": "Tamil Nadu", "district": "Kanchipuram", "latitude": 12.9820, "longitude": 79.9740, "road_type": "national_highway", "speed_limit": 90, "observed_avg_speed": 105, "aadt": 80000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "straight", "dominant_cause": "High-speed industrial worker crossing & truck speeding", "vulnerable_user_density": "high", "historical_crashes_3yr": 37, "fatalities_3yr": 27, "injuries_3yr": 31, "morth_blackspot_id": "BS-TN-002"},
    {"id": 18, "name": "Madhuravoyal Bypass Junction, NH-4", "corridor": "Chennai Bypass / NH-4", "state": "Tamil Nadu", "district": "Chennai", "latitude": 13.0640, "longitude": 80.1650, "road_type": "national_highway", "speed_limit": 70, "observed_avg_speed": 86, "aadt": 110000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "flyover_merge", "dominant_cause": "Two-wheeler blind merge & night freight", "vulnerable_user_density": "high", "historical_crashes_3yr": 29, "fatalities_3yr": 17, "injuries_3yr": 34, "morth_blackspot_id": "BS-TN-003"},
    {"id": 19, "name": "Thoppur Ghat, Salem-Dharmapuri NH-44", "corridor": "NH-44", "state": "Tamil Nadu", "district": "Dharmapuri", "latitude": 11.9420, "longitude": 78.0720, "road_type": "national_highway", "speed_limit": 50, "observed_avg_speed": 78, "aadt": 60000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "steep_ghat_curve", "dominant_cause": "CRITICAL: Multiple-truck brake failure pileups", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 68, "fatalities_3yr": 49, "injuries_3yr": 74, "morth_blackspot_id": "BS-TN-004"},
    {"id": 20, "name": "Perundurai Bypass Curve, NH-544", "corridor": "NH-544 (Salem-Kochi)", "state": "Tamil Nadu", "district": "Erode", "latitude": 11.2740, "longitude": 77.5840, "road_type": "national_highway", "speed_limit": 90, "observed_avg_speed": 108, "aadt": 72000, "surface_condition": "dry", "lighting": "unlit_dark", "geometry": "sharp_curve", "dominant_cause": "Nighttime overspeeding & Median collision", "vulnerable_user_density": "low", "historical_crashes_3yr": 35, "fatalities_3yr": 24, "injuries_3yr": 29, "morth_blackspot_id": "BS-TN-005"},

    {"id": 21, "name": "Silk Board Junction, Hosur Road", "corridor": "Outer Ring Road / Hosur Road", "state": "Karnataka", "district": "Bengaluru Urban", "latitude": 12.9176, "longitude": 77.6234, "road_type": "urban_arterial", "speed_limit": 50, "observed_avg_speed": 58, "aadt": 175000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "complex_intersection", "dominant_cause": "Two-wheeler blind cut & bus blind spots", "vulnerable_user_density": "critical", "historical_crashes_3yr": 31, "fatalities_3yr": 14, "injuries_3yr": 39, "morth_blackspot_id": "BS-KA-001"},
    {"id": 22, "name": "Hebbal Flyover Loop Merge, Bellary Road", "corridor": "NH-44 (Airport Expressway)", "state": "Karnataka", "district": "Bengaluru Urban", "latitude": 13.0358, "longitude": 77.5970, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 95, "aadt": 150000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "merge_ramp", "dominant_cause": "Speeding airport cabs & two-wheeler squeeze", "vulnerable_user_density": "high", "historical_crashes_3yr": 36, "fatalities_3yr": 20, "injuries_3yr": 38, "morth_blackspot_id": "BS-KA-002"},
    {"id": 23, "name": "Electronic City Toll Gate, NH-44", "corridor": "Hosur Road / NH-44", "state": "Karnataka", "district": "Bengaluru Urban", "latitude": 12.8450, "longitude": 77.6600, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 96, "aadt": 120000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "toll_approach", "dominant_cause": "High-speed rear-end into queued vehicles", "vulnerable_user_density": "high", "historical_crashes_3yr": 28, "fatalities_3yr": 16, "injuries_3yr": 32, "morth_blackspot_id": "BS-KA-003"},
    {"id": 24, "name": "Nelamangala Toll Plaza Merge, NH-48", "corridor": "NH-48 (Tumakuru Road)", "state": "Karnataka", "district": "Bengaluru Rural", "latitude": 13.0980, "longitude": 77.3820, "road_type": "national_highway", "speed_limit": 90, "observed_avg_speed": 104, "aadt": 90000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "straight", "dominant_cause": "Late night truck freight & two-wheeler hit", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 43, "fatalities_3yr": 31, "injuries_3yr": 38, "morth_blackspot_id": "BS-KA-004"},
    {"id": 25, "name": "Shiradi Ghat, Mangaluru-Bengaluru NH-75", "corridor": "NH-75", "state": "Karnataka", "district": "Hassan", "latitude": 12.9200, "longitude": 75.6800, "road_type": "national_highway", "speed_limit": 40, "observed_avg_speed": 52, "aadt": 32000, "surface_condition": "wet", "lighting": "unlit_dark", "geometry": "sharp_hairpin_bend", "dominant_cause": "Monsoon mud-skid, heavy vehicle rollover", "vulnerable_user_density": "low", "historical_crashes_3yr": 38, "fatalities_3yr": 25, "injuries_3yr": 46, "morth_blackspot_id": "BS-KA-005"},

    {"id": 26, "name": "Medchal Junction, NH-44 Corridor", "corridor": "NH-44 (North Corridor)", "state": "Telangana", "district": "Medchal-Malkajgiri", "latitude": 17.6290, "longitude": 78.4810, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 98, "aadt": 95000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "unsignalized_intersection", "dominant_cause": "Highway speeding & Tractor crossing", "vulnerable_user_density": "high", "historical_crashes_3yr": 39, "fatalities_3yr": 26, "injuries_3yr": 34, "morth_blackspot_id": "BS-TS-001"},
    {"id": 27, "name": "Gachibowli ORR Interchange Exit 19", "corridor": "Hyderabad Outer Ring Road", "state": "Telangana", "district": "Hyderabad", "latitude": 17.4400, "longitude": 78.3480, "road_type": "expressway", "speed_limit": 100, "observed_avg_speed": 122, "aadt": 85000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "merge_ramp", "dominant_cause": "Sudden exit divergence at high speeds", "vulnerable_user_density": "low", "historical_crashes_3yr": 31, "fatalities_3yr": 19, "injuries_3yr": 28, "morth_blackspot_id": "BS-TS-002"},
    {"id": 28, "name": "Hayathnagar Chintalkunta Junction, NH-65", "corridor": "NH-65 (Hyderabad-Vijayawada)", "state": "Telangana", "district": "Ranga Reddy", "latitude": 17.3210, "longitude": 78.6010, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 95, "aadt": 88000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "unsignalized_intersection", "dominant_cause": "Pedestrian hit & Wrong-side bike entry", "vulnerable_user_density": "critical", "historical_crashes_3yr": 37, "fatalities_3yr": 24, "injuries_3yr": 36, "morth_blackspot_id": "BS-TS-003"},
    {"id": 29, "name": "Benz Circle, Vijayawada, NH-16", "corridor": "NH-16 / MG Road", "state": "Andhra Pradesh", "district": "NTR", "latitude": 16.5010, "longitude": 80.6480, "road_type": "national_highway", "speed_limit": 60, "observed_avg_speed": 72, "aadt": 120000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "flyover_merge", "dominant_cause": "Two-wheeler side collisions & bus blind spots", "vulnerable_user_density": "high", "historical_crashes_3yr": 34, "fatalities_3yr": 18, "injuries_3yr": 41, "morth_blackspot_id": "BS-AP-001"},
    {"id": 30, "name": "Anakapalle Bypass Curve, NH-16", "corridor": "NH-16", "state": "Andhra Pradesh", "district": "Anakapalli", "latitude": 17.6890, "longitude": 83.0040, "road_type": "national_highway", "speed_limit": 90, "observed_avg_speed": 106, "aadt": 75000, "surface_condition": "dry", "lighting": "unlit_dark", "geometry": "sharp_curve", "dominant_cause": "Nighttime freight speed & rollover", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 42, "fatalities_3yr": 30, "injuries_3yr": 35, "morth_blackspot_id": "BS-AP-002"},

    {"id": 31, "name": "Edappally Toll Bypass Junction, NH-66", "corridor": "NH-66 / NH-544", "state": "Kerala", "district": "Ernakulam", "latitude": 10.0261, "longitude": 76.3082, "road_type": "national_highway", "speed_limit": 50, "observed_avg_speed": 64, "aadt": 125000, "surface_condition": "wet", "lighting": "lit_streetlights", "geometry": "complex_intersection", "dominant_cause": "Monsoon skidding & dense pedestrian crossing", "vulnerable_user_density": "critical", "historical_crashes_3yr": 46, "fatalities_3yr": 18, "injuries_3yr": 62, "morth_blackspot_id": "BS-KL-001"},
    {"id": 32, "name": "Vyttila Mobility Hub Junction", "corridor": "NH-66 Kochi Bypass", "state": "Kerala", "district": "Ernakulam", "latitude": 9.9670, "longitude": 76.3210, "road_type": "national_highway", "speed_limit": 50, "observed_avg_speed": 62, "aadt": 130000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "complex_intersection", "dominant_cause": "Interstate bus blind turning & bike collision", "vulnerable_user_density": "critical", "historical_crashes_3yr": 38, "fatalities_3yr": 15, "injuries_3yr": 54, "morth_blackspot_id": "BS-KL-002"},
    {"id": 33, "name": "Kuthiran Tunnel Approach, NH-544", "corridor": "NH-544", "state": "Kerala", "district": "Thrissur", "latitude": 10.5680, "longitude": 76.3980, "road_type": "national_highway", "speed_limit": 60, "observed_avg_speed": 78, "aadt": 70000, "surface_condition": "wet", "lighting": "poor_lighting", "geometry": "blind_turn", "dominant_cause": "Torrential monsoon rain skidding & truck jackknifing", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 41, "fatalities_3yr": 22, "injuries_3yr": 49, "morth_blackspot_id": "BS-KL-003"},

    {"id": 34, "name": "Narol Circle, NH-48 / Ring Road", "corridor": "NH-48", "state": "Gujarat", "district": "Ahmedabad", "latitude": 22.9730, "longitude": 72.6050, "road_type": "national_highway", "speed_limit": 60, "observed_avg_speed": 74, "aadt": 140000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "roundabout", "dominant_cause": "Industrial heavy truck mix & two-wheeler blind cut", "vulnerable_user_density": "high", "historical_crashes_3yr": 35, "fatalities_3yr": 21, "injuries_3yr": 38, "morth_blackspot_id": "BS-GJ-001"},
    {"id": 35, "name": "Golden Bridge Approach, Bharuch, NH-48", "corridor": "NH-48 (Ahmedabad-Mumbai)", "state": "Gujarat", "district": "Bharuch", "latitude": 21.7050, "longitude": 72.9980, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 98, "aadt": 95000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "bridge_approach", "dominant_cause": "Chemical tanker freight speeding & tailgating", "vulnerable_user_density": "low", "historical_crashes_3yr": 39, "fatalities_3yr": 29, "injuries_3yr": 32, "morth_blackspot_id": "BS-GJ-002"},
    {"id": 36, "name": "Transport Nagar Bypass, Jaipur, NH-21", "corridor": "NH-21 / Jaipur Bypass", "state": "Rajasthan", "district": "Jaipur", "latitude": 26.9020, "longitude": 75.8450, "road_type": "national_highway", "speed_limit": 70, "observed_avg_speed": 88, "aadt": 85000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "unsignalized_intersection", "dominant_cause": "Desert highway high-speed freight & pedestrian crossing", "vulnerable_user_density": "high", "historical_crashes_3yr": 36, "fatalities_3yr": 25, "injuries_3yr": 33, "morth_blackspot_id": "BS-RJ-001"},
    {"id": 37, "name": "Kishangarh Marble Slurry Stretch, NH-48", "corridor": "NH-48", "state": "Rajasthan", "district": "Ajmer", "latitude": 26.5750, "longitude": 74.8620, "road_type": "national_highway", "speed_limit": 90, "observed_avg_speed": 112, "aadt": 75000, "surface_condition": "poor_friction", "lighting": "unlit_dark", "geometry": "straight", "dominant_cause": "Slippery dust surface skid & excessive speed", "vulnerable_user_density": "low", "historical_crashes_3yr": 43, "fatalities_3yr": 32, "injuries_3yr": 36, "morth_blackspot_id": "BS-RJ-002"},

    {"id": 38, "name": "Kona Expressway Toll Junction, Howrah", "corridor": "NH-12 / Kona Expressway", "state": "West Bengal", "district": "Howrah", "latitude": 22.5850, "longitude": 88.2910, "road_type": "national_highway", "speed_limit": 60, "observed_avg_speed": 76, "aadt": 115000, "surface_condition": "wet", "lighting": "poor_lighting", "geometry": "flyover_merge", "dominant_cause": "Port container freight & auto-rickshaw conflict", "vulnerable_user_density": "high", "historical_crashes_3yr": 38, "fatalities_3yr": 24, "injuries_3yr": 41, "morth_blackspot_id": "BS-WB-001"},
    {"id": 39, "name": "Dankuni Toll Plaza, NH-19", "corridor": "NH-19 (Delhi-Kolkata)", "state": "West Bengal", "district": "Hooghly", "latitude": 22.6850, "longitude": 88.3050, "road_type": "national_highway", "speed_limit": 80, "observed_avg_speed": 96, "aadt": 90000, "surface_condition": "dry", "lighting": "poor_lighting", "geometry": "toll_approach", "dominant_cause": "Stationary vehicle rear-end & pedestrian hit", "vulnerable_user_density": "moderate", "historical_crashes_3yr": 34, "fatalities_3yr": 22, "injuries_3yr": 30, "morth_blackspot_id": "BS-WB-002"},
    {"id": 40, "name": "Palasuni Overbridge Curve, Bhubaneswar", "corridor": "NH-16", "state": "Odisha", "district": "Khordha", "latitude": 20.3120, "longitude": 85.8640, "road_type": "national_highway", "speed_limit": 70, "observed_avg_speed": 85, "aadt": 92000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "sharp_curve", "dominant_cause": "Two-wheeler skid & truck blind turn", "vulnerable_user_density": "high", "historical_crashes_3yr": 32, "fatalities_3yr": 19, "injuries_3yr": 37, "morth_blackspot_id": "BS-OD-001"},
    {"id": 41, "name": "Misrod Bypass, Bhopal, NH-46", "corridor": "NH-46 / Hoshangabad Road", "state": "Madhya Pradesh", "district": "Bhopal", "latitude": 23.1650, "longitude": 77.4620, "road_type": "national_highway", "speed_limit": 70, "observed_avg_speed": 88, "aadt": 80000, "surface_condition": "potholes", "lighting": "poor_lighting", "geometry": "unsignalized_intersection", "dominant_cause": "Pothole avoidance swerving & two-wheeler hit", "vulnerable_user_density": "high", "historical_crashes_3yr": 37, "fatalities_3yr": 23, "injuries_3yr": 39, "morth_blackspot_id": "BS-MP-001"},
    {"id": 42, "name": "Bhanwarkuan Square, Indore, AB Road", "corridor": "AB Road / NH-52", "state": "Madhya Pradesh", "district": "Indore", "latitude": 22.6880, "longitude": 75.8610, "road_type": "urban_arterial", "speed_limit": 50, "observed_avg_speed": 62, "aadt": 125000, "surface_condition": "dry", "lighting": "lit_streetlights", "geometry": "complex_intersection", "dominant_cause": "Student two-wheeler density & BRTS crossing", "vulnerable_user_density": "critical", "historical_crashes_3yr": 29, "fatalities_3yr": 14, "injuries_3yr": 43, "morth_blackspot_id": "BS-MP-002"}
]

zones_extra = [
    ("Punjab", "Ludhiana", "Sherpur Chowk, GT Road NH-44", 30.8920, 75.8920, "national_highway", "Winter Fog & High Speed", 36, 25, 29),
    ("Punjab", "Amritsar", "Golden Gate Entry NH-3", 31.6210, 74.9250, "national_highway", "Tractor trolley rear-end", 28, 19, 24),
    ("Haryana", "Panipat", "Panipat Toll Plaza NH-44", 29.3820, 76.9620, "national_highway", "Overspeeding & Fog", 41, 30, 35),
    ("Haryana", "Karnal", "Oasis Complex Curve NH-44", 29.6820, 76.9850, "national_highway", "High speed passenger car collision", 32, 22, 28),
    ("Uttar Pradesh", "Varanasi", "Mohansarai Bypass NH-19", 25.2750, 82.8820, "national_highway", "Pedestrian crossing & night trucks", 35, 24, 31),
    ("Uttar Pradesh", "Prayagraj", "Naini Bridge Approach NH-30", 25.4120, 81.8750, "national_highway", "Bridge narrow merge & speeding", 29, 18, 26),
    ("Uttar Pradesh", "Bareilly", "Fatehganj Bypass NH-24", 28.5200, 79.3200, "national_highway", "Unlit tractors & winter fog", 33, 23, 27),
    ("Uttar Pradesh", "Meerut", "Partapur Interchange, Delhi-Meerut Expressway", 28.9200, 77.6200, "expressway", "High speed merge & lane drifting", 37, 26, 33),
    ("Maharashtra", "Nagpur", "Wadi Junction, Amravati Road NH-53", 21.1450, 79.0120, "national_highway", "Heavy mining trucks & bikes", 34, 21, 36),
    ("Maharashtra", "Nashik", "Dwarka Circle NH-60", 19.9920, 73.7920, "national_highway", "Industrial traffic & two-wheelers", 31, 19, 33),
    ("Maharashtra", "Kolhapur", "Shiroli Naka NH-48", 16.7320, 74.2620, "national_highway", "Sugarcane tractor collisions", 30, 20, 25),
    ("Tamil Nadu", "Madurai", "Kappalur Toll Plaza NH-44", 9.8520, 78.0250, "national_highway", "High speed night buses & trucks", 38, 28, 32),
    ("Tamil Nadu", "Coimbatore", "Neelambur Bypass NH-544", 11.0620, 77.0850, "national_highway", "Two-wheeler speeding & merge conflict", 33, 21, 35),
    ("Tamil Nadu", "Tiruchirappalli", "Palpannai Roundabout NH-83", 10.8250, 78.7120, "national_highway", "Heavy container vehicles & bikes", 28, 17, 30),
    ("Karnataka", "Mysuru", "Columbia Asia Hospital Junction, Mysuru Expressway", 12.3520, 76.6620, "expressway", "Expressway terminus high-speed overshoot", 39, 24, 41),
    ("Karnataka", "Hubballi", "Gabbur Toll Cross NH-48", 15.3120, 75.1620, "national_highway", "Bypass intersection speeding", 32, 22, 28),
    ("Karnataka", "Belagavi", "Kakati Bypass Curve NH-48", 15.9250, 74.5420, "national_highway", "Downhill gradient & wet weather skid", 34, 25, 29),
    ("Telangana", "Warangal", "Madikonda Junction NH-163", 17.9250, 79.5250, "national_highway", "Two-wheelers & high-speed buses", 27, 18, 25),
    ("Telangana", "Nizamabad", "Dichpally Crossroad NH-44", 18.5820, 78.2120, "national_highway", "Unsignalized NH crossing", 29, 20, 24),
    ("Andhra Pradesh", "Tirupati", "Renigunta Airport Road Junction", 13.6320, 79.4850, "national_highway", "Pilgrim bus traffic & speeding cars", 28, 19, 31),
    ("Andhra Pradesh", "Guntur", "Autonagar Crossroad NH-16", 16.3250, 80.4620, "national_highway", "Commercial loading & bike conflicts", 31, 21, 29),
    ("Kerala", "Kozhikode", "Thondayad Bypass Junction NH-66", 11.2620, 75.8120, "national_highway", "Heavy monsoon rain & two-wheeler skid", 35, 16, 48),
    ("Kerala", "Kollam", "Kavanad Bypass Curve NH-66", 8.9250, 76.5720, "national_highway", "Narrow coastal highway & head-on crash", 29, 14, 38),
    ("Rajasthan", "Udaipur", "Debari Zinc Smelter Curve NH-48", 24.6020, 73.7850, "national_highway", "Sharp curve in hilly section & trucks", 33, 24, 27),
    ("Rajasthan", "Jodhpur", "Mandore Road Bypass", 26.3420, 73.0450, "state_highway", "High speed unlit desert road", 26, 17, 22),
    ("Gujarat", "Surat", "Kadodara Char Rasta NH-48", 21.1820, 72.9620, "national_highway", "Textile transport & worker crossing", 37, 23, 41),
    ("Gujarat", "Vadodara", "Golden Crossroads NH-48", 22.3420, 73.2250, "national_highway", "Freight bypass & two-wheeler traffic", 32, 20, 31),
    ("Bihar", "Patna", "Didarganj Toll Plaza NH-31", 25.5620, 85.2620, "national_highway", "Overloaded trucks & auto-rickshaws", 36, 26, 32),
    ("Bihar", "Muzaffarpur", "Bhagwanpur Chowk NH-28", 26.1150, 85.3620, "national_highway", "Pedestrian market & highway speeding", 34, 24, 30),
    ("Assam", "Guwahati", "Jalukbari Rotary NH-27", 26.1520, 91.6620, "national_highway", "Major confluence of East-West corridor", 30, 18, 35),
    ("Uttarakhand", "Dehradun", "Mohand Pass Ghat NH-307", 30.2150, 77.9250, "national_highway", "Blind hairpin bends in Shivalik hills", 31, 22, 28),
    ("Himachal Pradesh", "Shimla", "Taradevi Curve NH-5", 31.0820, 77.1350, "national_highway", "Ghat descent & tourist vehicle brake fail", 27, 19, 24)
]

cur_id = 43
for s, d, n, lat, lon, rtype, cause, c3, f3, i3 in zones_extra:
    blackspots.append({
        "id": cur_id,
        "name": n,
        "corridor": n.split(", ")[-1] if ", " in n else "Corridor",
        "state": s,
        "district": d,
        "latitude": lat,
        "longitude": lon,
        "road_type": rtype,
        "speed_limit": 80 if rtype == "national_highway" else 100 if rtype == "expressway" else 60,
        "observed_avg_speed": 92 if rtype == "national_highway" else 115 if rtype == "expressway" else 74,
        "aadt": 85000,
        "surface_condition": "wet" if s in ["Kerala", "Assam"] else "dry",
        "lighting": "poor_lighting",
        "geometry": "sharp_curve" if "Curve" in n or "Ghat" in n else "unsignalized_intersection" if "Chowk" in n or "Junction" in n else "straight",
        "dominant_cause": cause,
        "vulnerable_user_density": "critical" if s in ["Kerala", "Tamil Nadu", "West Bengal"] else "high",
        "historical_crashes_3yr": c3,
        "fatalities_3yr": f3,
        "injuries_3yr": i3,
        "morth_blackspot_id": f"BS-{s[:2].upper()}-{cur_id:03d}"
    })
    cur_id += 1

with open(os.path.join(DATA_DIR, 'indian_blackspots_database.json'), 'w', encoding='utf-8') as f:
    json.dump(blackspots, f, indent=2)

# 6. Trauma Care & Emergency Dispatch Centers (Golden Hour Network)
trauma_centers = [
    {"name": "AIIMS Apex Trauma Centre, New Delhi", "city": "New Delhi", "state": "Delhi", "latitude": 28.5684, "longitude": 77.2064, "level": "Level-1", "ambulances": 14, "icu_beds": 80, "avg_response_min": 9},
    {"name": "KEM Hospital & Trauma Centre, Mumbai", "city": "Mumbai", "state": "Maharashtra", "latitude": 19.0022, "longitude": 72.8428, "level": "Level-1", "ambulances": 12, "icu_beds": 65, "avg_response_min": 11},
    {"name": "NIMHANS Emergency & Trauma, Bengaluru", "city": "Bengaluru", "state": "Karnataka", "latitude": 12.9388, "longitude": 77.5959, "level": "Level-1", "ambulances": 10, "icu_beds": 50, "avg_response_min": 12},
    {"name": "Rajiv Gandhi Government General Hospital, Chennai", "city": "Chennai", "state": "Tamil Nadu", "latitude": 13.0805, "longitude": 80.2785, "level": "Level-1", "ambulances": 16, "icu_beds": 90, "avg_response_min": 8},
    {"name": "NIMS Hospital & Emergency Care, Hyderabad", "city": "Hyderabad", "state": "Telangana", "latitude": 17.4223, "longitude": 78.4552, "level": "Level-1", "ambulances": 11, "icu_beds": 55, "avg_response_min": 10},
    {"name": "SMS Hospital & Trauma Centre, Jaipur", "city": "Jaipur", "state": "Rajasthan", "latitude": 26.8988, "longitude": 75.8155, "level": "Level-1", "ambulances": 9, "icu_beds": 45, "avg_response_min": 11},
    {"name": "Civil Hospital Trauma Centre, Ahmedabad", "city": "Ahmedabad", "state": "Gujarat", "latitude": 23.0520, "longitude": 72.6020, "level": "Level-1", "ambulances": 12, "icu_beds": 60, "avg_response_min": 10},
    {"name": "SSKM Hospital Trauma Centre, Kolkata", "city": "Kolkata", "state": "West Bengal", "latitude": 22.5390, "longitude": 88.3440, "level": "Level-1", "ambulances": 10, "icu_beds": 50, "avg_response_min": 13},
    {"name": "KGMU Trauma Centre, Lucknow", "city": "Lucknow", "state": "Uttar Pradesh", "latitude": 26.8680, "longitude": 80.9160, "level": "Level-1", "ambulances": 14, "icu_beds": 70, "avg_response_min": 9},
    {"name": "Government Medical College Trauma, Kozhikode", "city": "Kozhikode", "state": "Kerala", "latitude": 11.2720, "longitude": 75.8360, "level": "Level-2", "ambulances": 8, "icu_beds": 40, "avg_response_min": 12},
    {"name": "AIIMS Rishikesh Trauma Centre, Haridwar Bypass", "city": "Rishikesh", "state": "Uttarakhand", "latitude": 30.0750, "longitude": 78.2880, "level": "Level-1", "ambulances": 7, "icu_beds": 35, "avg_response_min": 14},
    {"name": "PGI Emergency & Trauma Centre, Chandigarh", "city": "Chandigarh", "state": "Chandigarh", "latitude": 30.7650, "longitude": 76.7760, "level": "Level-1", "ambulances": 10, "icu_beds": 60, "avg_response_min": 9}
]

with open(os.path.join(DATA_DIR, 'trauma_care_centers.json'), 'w', encoding='utf-8') as f:
    json.dump(trauma_centers, f, indent=2)

print("Datasets built successfully!")
