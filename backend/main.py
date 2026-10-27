from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from backend.config import settings
from backend.routers import accidents
from backend.routers import auth as auth_router
from backend.routers import potholes as potholes_router
from backend.database import engine, Base, SessionLocal
from backend.models import Accident, User, PotholeRecord
from backend.analytics import seed_demo
from backend.auth import get_password_hash
from backend.routers.potholes import seed_pothole_samples

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo(db)
        # Seed default users for each role (if not already present)
        _seed_default_users(db)
        # Seed initial audited Indian highway blackspot pothole samples
        try:
            seed_pothole_samples(db)
        except Exception as pe:
            print(f"Startup pothole seeding note: {pe}")
    except Exception as e:
        print(f"Startup database seeding note: {e}")
    finally:
        db.close()
    yield


def _seed_default_users(db):
    """Create demo users for each role if they don't already exist."""
    demo_users = [
        {"username": "admin", "password": "admin123", "role": "government", "full_name": "Government Admin"},
        {"username": "contractor1", "password": "contractor123", "role": "contractor", "full_name": "Highway Contractor"},
        {"username": "citizen", "password": "citizen123", "role": "user", "full_name": "Public Citizen"},
    ]
    for u in demo_users:
        if not db.query(User).filter(User.username == u["username"]).first():
            user = User(
                username=u["username"],
                hashed_password=get_password_hash(u["password"]),
                full_name=u["full_name"],
                role=u["role"],
            )
            db.add(user)
    db.commit()

app = FastAPI(
    title='RoadSafe India — AI Road Safety Intelligence Platform',
    version='2.6.0',
    description='AI-Powered Road Safety Intelligence, Pothole Detection & Defect Intelligence, Risk Mapping, Explainable Causal Analysis, and Counterfactual Intervention Simulation for Indian Authorities (Problem Statement 03: Transport: RoadSafe India).',
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Register API routers
app.include_router(auth_router.router, prefix='/api/v1/auth', tags=['Authentication'])
app.include_router(accidents.router, prefix='/api/v1/accidents', tags=['Road Safety Intelligence'])
app.include_router(potholes_router.router, prefix='/api/v1/potholes', tags=['Pothole & Defect Intelligence'])
app.include_router(potholes_router.router, prefix='/api/potholes', tags=['Pothole & Defect Intelligence (Direct)'])

@app.get('/api/v1/health')
@app.get('/health')
def health():
    return {
        'status': 'healthy',
        'service': 'RoadSafe India — Safety Intelligence Grid',
        'version': '2.6.0'
    }

@app.get('/api/v1/meta')
def meta():
    return {
        'name': 'RoadSafe India',
        'problem_statement': 'Problem Statement No. 3 - Transport: RoadSafe India',
        'team_id': 'Team_015',
        'pan_india_coverage': 'All 36 States and Union Territories with 2018-2023 MoRTH/NCRB crash longitudinal metrics',
        'pothole_detection_module': 'AI-Based Pothole Detection, Bounding Box Localization, Severity Heuristics & Repair Pipeline',
        'six_core_answers': {
            '1_where': 'Interactive GIS Risk Map with 95+ geocoded blackspots across all 36 States & UTs (NH-44, NH-48, NH-66 and Expressways)',
            '2_why': 'Explainable AI Feature Attribution & MoRTH Cause of Accident Breakdown (69.6% Overspeeding)',
            '3_who_vulnerable': 'Vulnerable Road Users (VRU): Two-wheelers (44.5% fatalities) and Pedestrians (19.5% fatalities)',
            '4_when_highest': '24-Hour Diurnal Peak (18:00 - 21:00 dusk rush + 21:00 - 03:00 freight) & Monsoon/Winter Fog seasons',
            '5_what_intervention': 'Ranked IRC-Standard Engineering (IRC:103, IRC:73), ITS Automated Enforcement, and EMS Golden Hour Network',
            '6_predict_impact': 'Interactive Counterfactual What-If Simulator projecting crash reduction %, lives saved/yr, and safety ROI'
        }
    }

# Static files & Uploads serving
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(root_dir, 'frontend')

# Mount uploads directory for images
if os.path.isdir(settings.UPLOAD_DIR):
    app.mount('/uploads', StaticFiles(directory=settings.UPLOAD_DIR), name='uploads')

if os.path.isdir(frontend_dir):
    app.mount('/static', StaticFiles(directory=frontend_dir), name='static')

@app.get('/')
def serve_index():
    if os.path.isfile(os.path.join(root_dir, 'index.html')):
        return FileResponse(os.path.join(root_dir, 'index.html'))
    return FileResponse(os.path.join(frontend_dir, 'index.html'))
