# Road Safety AI System

Transform India into a global leader in AI-driven road safety by creating an equitable, predictive system that prevents accidents before they occur across all geographic regions.

## Overview

The Road Safety AI System is a backend API designed for transportation officials, district administrators, policy makers, and safety enforcement agencies responsible for road infrastructure and accident prevention across India.

## Target Audience

- Transportation officials
- District administrators
- Policy makers
- Safety enforcement agencies

## Core Features

- **Accident Record Management**: Complete CRUD operations for accident data
- **Geographic Filtering**: Filter accidents by state and district
- **Severity Tracking**: Categorize and track accident severity levels
- **Statistical Analysis**: Get comprehensive accident statistics and trends
- **Real-time Data**: Track casualties, injuries, and fatalities

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 (SQLite default, PostgreSQL/MySQL supported)
- **Validation**: Pydantic 2.5.0
- **Server**: Uvicorn 0.24.0

## Architecture

Modular Monolith architecture with clear separation of concerns:
- `backend/main.py` - Application entry point
- `backend/models.py` - Database models
- `backend/schemas.py` - Pydantic schemas for validation
- `backend/routers/` - API route handlers
- `backend/config.py` - Configuration management
- `backend/database.py` - Database connection and session management

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Linux/Mac:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

4. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

5. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env` file and update configuration as needed, especially:
- `DATABASE_URL` for production database
- `SECRET_KEY` for security
- `ALLOWED_ORIGINS` for CORS

## Running the Application

### Development Mode

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Production Mode

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

### Accident Management
- `POST /api/v1/accidents/` - Create new accident record
- `GET /api/v1/accidents/` - List accidents (with pagination and filters)
- `GET /api/v1/accidents/{accident_id}` - Get specific accident
- `PUT /api/v1/accidents/{accident_id}` - Update accident record
- `DELETE /api/v1/accidents/{accident_id}` - Delete accident record

### Statistics
- `GET /api/v1/accidents/stats/summary` - Get accident statistics

### Query Parameters for Listing

- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 50, max: 100)
- `state` - Filter by state
- `district` - Filter by district
- `severity` - Filter by severity (minor, moderate, severe, fatal)
- `accident_type` - Filter by accident type

## Data Models

### Accident Record

```json
{
  "location": "NH-44, Near Toll Plaza",
  "latitude": 28.7041,
  "longitude": 77.1025,
  "state": "Delhi",
  "district": "New Delhi",
  "accident_type": "collision",
  "severity": "moderate",
  "casualties": 2,
  "injuries": 2,
  "fatalities": 0,
  "weather_condition": "Clear",
  "road_condition": "Dry",
  "time_of_day": "Morning",
  "description": "Two-vehicle collision at intersection",
  "contributing_factors": "Speeding, Poor visibility",
  "reported_by": "Traffic Police"
}
```

### Severity Levels
- `minor` - Minor accidents with minimal damage
- `moderate` - Moderate accidents with injuries
- `severe` - Severe accidents with serious injuries
- `fatal` - Fatal accidents with deaths

### Accident Types
- `collision` - Vehicle collision
- `pedestrian` - Pedestrian involved
- `vehicle_rollover` - Vehicle rollover
- `head_on` - Head-on collision
- `rear_end` - Rear-end collision
- `side_impact` - Side impact collision
- `other` - Other types

## Database

The application uses SQLite by default for development. For production, configure PostgreSQL or MySQL in the `.env` file:

**PostgreSQL:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/road_safety_db
```

**MySQL:**
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/road_safety_db
```

The database tables are automatically created on application startup.

## Security

- Environment variables for sensitive configuration
- Input validation using Pydantic
- SQL injection prevention through SQLAlchemy ORM
- CORS configuration for API access control
- Logging for audit trails

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       └── accidents.py     # Accident endpoints
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Development

### Adding New Features

1. Define models in `backend/models.py`
2. Create schemas in `backend/schemas.py`
3. Implement routes in `backend/routers/`
4. Register router in `backend/main.py`

### Code Quality

- Follow PEP 8 style guidelines
- Add type hints for better code clarity
- Include docstrings for functions and classes
- Use meaningful variable and function names

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL in `.env` file
- Ensure database server is running (for PostgreSQL/MySQL)
- Check database credentials and permissions

### Import Errors
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r backend/requirements.txt`

### Port Already in Use
- Change the port: `uvicorn backend.main:app --port 8001`
- Or kill the process using port 8000

## Support

For issues and questions, refer to the API documentation at `/docs` endpoint.

## License

This project is part of the Road Safety AI initiative for India.
