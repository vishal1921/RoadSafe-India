from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from backend.config import settings
from backend.routers import accidents
from backend.database import engine, Base, SessionLocal
from backend.models import Accident
from backend.analytics import seed_demo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo(db)
    except Exception as e:
        print(f"Startup database seeding note: {e}")
    finally:
        db.close()
    yield

app = FastAPI(
    title='RoadSafe India — AI Road Safety Intelligence Platform',
    version='2.5.0',
    description='AI-Powered Road Safety Intelligence, Risk Mapping, Explainable Causal Analysis, Diurnal Risk Profiling, and Counterfactual Intervention Simulation for Indian Authorities (Problem Statement 03: Transport: RoadSafe India).',
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
app.include_router(accidents.router, prefix='/api/v1/accidents', tags=['Road Safety Intelligence'])

@app.get('/api/v1/health')
@app.get('/health')
def health():
    return {
        'status': 'healthy',
        'service': 'RoadSafe India — Safety Intelligence Grid',
        'version': '2.5.0'
    }

@app.get('/api/v1/meta')
def meta():
    return {
        'name': 'RoadSafe India',
        'problem_statement': 'Problem Statement No. 3 - Transport: RoadSafe India',
        'team_id': 'Team_015',
        'pan_india_coverage': 'All 36 States and Union Territories with 2018-2023 MoRTH/NCRB crash longitudinal metrics',
        'six_core_answers': {
            '1_where': 'Interactive GIS Risk Map with 95+ geocoded blackspots across all 36 States & UTs (NH-44, NH-48, NH-66 and Expressways)',
            '2_why': 'Explainable AI Feature Attribution & MoRTH Cause of Accident Breakdown (69.6% Overspeeding)',
            '3_who_vulnerable': 'Vulnerable Road Users (VRU): Two-wheelers (44.5% fatalities) and Pedestrians (19.5% fatalities)',
            '4_when_highest': '24-Hour Diurnal Peak (18:00 - 21:00 dusk rush + 21:00 - 03:00 freight) & Monsoon/Winter Fog seasons',
            '5_what_intervention': 'Ranked IRC-Standard Engineering (IRC:103, IRC:73), ITS Automated Enforcement, and EMS Golden Hour Network',
            '6_predict_impact': 'Interactive Counterfactual What-If Simulator projecting crash reduction %, lives saved/yr, and safety ROI'
        }
    }

# Static files & Frontend serving
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(root_dir, 'frontend')

if os.path.isdir(frontend_dir):
    app.mount('/static', StaticFiles(directory=frontend_dir), name='static')
    @app.get('/')
    def serve_frontend_index():
        return FileResponse(os.path.join(frontend_dir, 'index.html'))
elif os.path.isfile(os.path.join(root_dir, 'index.html')):
    @app.get('/')
    def serve_root_index():
        return FileResponse(os.path.join(root_dir, 'index.html'))
