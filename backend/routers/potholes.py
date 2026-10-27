"""
FastAPI router for Pothole Detection & Road Defect Intelligence.
Endpoints:
- POST /detect (upload image, run detection, save record)
- GET / (list potholes with filters)
- GET /{pothole_id} (get single pothole)
- PATCH /{pothole_id}/status (update verification or repair status)
- GET /analytics (aggregated summary stats and distributions)
- POST /seed-samples (populate initial verified blackspot pothole samples)
"""

import os
import json
import uuid
import shutil
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.database import get_db
from backend.models import PotholeRecord
from backend.config import settings
from backend.pothole_detector import pothole_detector
from backend.schemas_potholes import (
    PotholeDetectionResponse,
    PotholeStatusUpdate,
    PotholeAnalyticsResponse
)

router = APIRouter()

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_BYTES = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024


@router.post("/detect", response_model=PotholeDetectionResponse, status_code=status.HTTP_201_CREATED)
async def detect_pothole_image(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    road_name: Optional[str] = Form("National Highway Corridor"),
    state: Optional[str] = Form("Maharashtra"),
    district: Optional[str] = Form("Pune"),
    reporter: Optional[str] = Form("RoadSafe Field Auditor"),
    db: Session = Depends(get_db)
):
    """
    Accepts road image upload (JPG, JPEG, PNG), runs AI pothole detector,
    estimates explainable severity, saves to database, and returns annotated results.
    """
    # 1. Validate file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format '{ext}'. Only JPG, JPEG, and PNG images are allowed."
        )

    # 2. Save original image to disk
    original_dir = os.path.join(settings.UPLOAD_DIR, "potholes", "original")
    os.makedirs(original_dir, exist_ok=True)
    
    unique_name = f"road_{uuid.uuid4().hex[:10]}{ext}"
    orig_path = os.path.join(original_dir, unique_name)
    
    bytes_written = 0
    try:
        with open(orig_path, "wb") as buffer:
            while chunk := await file.read(1024 * 512):
                bytes_written += len(chunk)
                if bytes_written > MAX_FILE_BYTES:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Uploaded file exceeds {settings.MAX_IMAGE_SIZE_MB}MB size limit."
                    )
                buffer.write(chunk)
    except HTTPException:
        if os.path.exists(orig_path):
            os.remove(orig_path)
        raise
    except Exception as e:
        if os.path.exists(orig_path):
            os.remove(orig_path)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save image: {e}")

    # 3. Run AI Pothole Detection
    try:
        detection_result = pothole_detector.detect_potholes(orig_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Inference error during pothole detection: {str(e)}"
        )

    # 4. Generate persistent record ID
    year = datetime.now().year
    count_today = db.query(PotholeRecord).count() + 1
    pothole_code = f"PH-{year}-{count_today:04d}"

    # 5. Persist to Database
    record = PotholeRecord(
        pothole_id=pothole_code,
        image_path=f"/uploads/potholes/original/{unique_name}",
        annotated_image_path=detection_result["relative_annotated_url"],
        latitude=latitude,
        longitude=longitude,
        road_name=road_name,
        state=state,
        district=district,
        pothole_count=detection_result["pothole_count"],
        bounding_boxes_json=json.dumps(detection_result["detections"]),
        detection_confidence=detection_result["avg_confidence"],
        severity=detection_result["severity"],
        severity_method=detection_result["severity_method"],
        severity_reason=detection_result["severity_reason"],
        verification_status="unverified",
        repair_status="reported",
        reporter=reporter,
        model_id=detection_result["model_id"],
        processing_time_ms=detection_result["processing_time_ms"],
        is_demo=detection_result["is_demo"]
    )
    
    db.add(record)
    db.commit()
    db.refresh(record)

    return PotholeDetectionResponse(
        pothole_id=record.pothole_id,
        pothole_count=record.pothole_count,
        detections=detection_result["detections"],
        avg_confidence=record.detection_confidence,
        severity=record.severity,
        severity_method=record.severity_method,
        severity_reason=record.severity_reason or "",
        image_url=record.image_path,
        annotated_image_url=record.annotated_image_path or record.image_path,
        latitude=record.latitude,
        longitude=record.longitude,
        road_name=record.road_name,
        state=record.state,
        verification_status=record.verification_status,
        repair_status=record.repair_status,
        model_id=record.model_id,
        processing_time_ms=record.processing_time_ms,
        is_demo=record.is_demo,
        detection_date=record.detection_date
    )


@router.get("/", response_model=List[PotholeDetectionResponse])
def list_potholes(
    severity: Optional[str] = None,
    verification_status: Optional[str] = None,
    repair_status: Optional[str] = None,
    state: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Returns list of detected potholes with optional status, state, and severity filtering."""
    query = db.query(PotholeRecord)
    
    if severity and severity != "All":
        query = query.filter(PotholeRecord.severity == severity.lower())
    if verification_status and verification_status != "All":
        query = query.filter(PotholeRecord.verification_status == verification_status.lower())
    if repair_status and repair_status != "All":
        query = query.filter(PotholeRecord.repair_status == repair_status.lower())
    if state and state != "All":
        query = query.filter(PotholeRecord.state.ilike(f"%{state}%"))

    records = query.order_by(desc(PotholeRecord.created_at)).offset(offset).limit(limit).all()

    output = []
    for r in records:
        boxes = []
        if r.bounding_boxes_json:
            try:
                boxes = json.loads(r.bounding_boxes_json)
            except Exception:
                boxes = []
        
        output.append(PotholeDetectionResponse(
            pothole_id=r.pothole_id,
            pothole_count=r.pothole_count,
            detections=boxes,
            avg_confidence=r.detection_confidence,
            severity=r.severity,
            severity_method=r.severity_method or "",
            severity_reason=r.severity_reason or "",
            image_url=r.image_path,
            annotated_image_url=r.annotated_image_path or r.image_path,
            latitude=r.latitude,
            longitude=r.longitude,
            road_name=r.road_name,
            state=r.state,
            verification_status=r.verification_status,
            repair_status=r.repair_status,
            model_id=r.model_id or "pothole-adapter-v1",
            processing_time_ms=r.processing_time_ms or 0.0,
            is_demo=bool(r.is_demo),
            detection_date=r.detection_date
        ))
    return output


@router.get("/analytics", response_model=PotholeAnalyticsResponse)
def get_pothole_analytics(db: Session = Depends(get_db)):
    """Returns defect analytics: counts, severity distribution, repair stages, and top corridors."""
    total = db.query(PotholeRecord).count()
    verified = db.query(PotholeRecord).filter(PotholeRecord.verification_status == "verified").count()
    high_priority = db.query(PotholeRecord).filter(PotholeRecord.severity.in_(["critical", "severe"])).count()
    repaired = db.query(PotholeRecord).filter(PotholeRecord.repair_status == "repaired").count()
    unresolved = total - repaired

    # Severity distribution
    sev_counts = {"critical": 0, "severe": 0, "moderate": 0, "minor": 0}
    for row in db.query(PotholeRecord.severity, func.count(PotholeRecord.id)).group_by(PotholeRecord.severity).all():
        if row[0] in sev_counts:
            sev_counts[row[0]] = row[1]

    # Repair status distribution
    repair_counts = {"reported": 0, "inspected": 0, "scheduled": 0, "in_progress": 0, "repaired": 0}
    for row in db.query(PotholeRecord.repair_status, func.count(PotholeRecord.id)).group_by(PotholeRecord.repair_status).all():
        if row[0] in repair_counts:
            repair_counts[row[0]] = row[1]

    # Top affected corridors
    top_corridors = []
    corridor_query = (
        db.query(PotholeRecord.road_name, PotholeRecord.state, func.count(PotholeRecord.id).label("defect_count"))
        .group_by(PotholeRecord.road_name, PotholeRecord.state)
        .order_by(desc("defect_count"))
        .limit(6)
        .all()
    )
    for c in corridor_query:
        if c[0]:
            top_corridors.append({
                "road_name": c[0],
                "state": c[1] or "National",
                "defect_count": c[2]
            })

    return PotholeAnalyticsResponse(
        total_detected=total,
        total_verified=verified,
        high_priority_count=high_priority,
        unresolved_count=unresolved,
        repaired_count=repaired,
        severity_distribution=sev_counts,
        repair_status_distribution=repair_counts,
        top_corridors=top_corridors,
        model_info={
            "model_path": settings.POTHOLE_MODEL_PATH,
            "weights_exist": os.path.exists(settings.POTHOLE_MODEL_PATH),
            "adapter_type": pothole_detector.model_type,
            "dataset_reference": settings.ROBOFLOW_DATASET_URL
        }
    )




@router.get("/{pothole_id}", response_model=PotholeDetectionResponse)
def get_pothole_detail(pothole_id: str, db: Session = Depends(get_db)):
    """Fetches full details for a single pothole detection record."""
    r = db.query(PotholeRecord).filter(PotholeRecord.pothole_id == pothole_id).first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pothole {pothole_id} not found.")

    boxes = []
    if r.bounding_boxes_json:
        try:
            boxes = json.loads(r.bounding_boxes_json)
        except Exception:
            boxes = []

    return PotholeDetectionResponse(
        pothole_id=r.pothole_id,
        pothole_count=r.pothole_count,
        detections=boxes,
        avg_confidence=r.detection_confidence,
        severity=r.severity,
        severity_method=r.severity_method or "",
        severity_reason=r.severity_reason or "",
        image_url=r.image_path,
        annotated_image_url=r.annotated_image_path or r.image_path,
        latitude=r.latitude,
        longitude=r.longitude,
        road_name=r.road_name,
        state=r.state,
        verification_status=r.verification_status,
        repair_status=r.repair_status,
        model_id=r.model_id or "pothole-adapter-v1",
        processing_time_ms=r.processing_time_ms or 0.0,
        is_demo=bool(r.is_demo),
        detection_date=r.detection_date
    )


@router.patch("/{pothole_id}/status", response_model=PotholeDetectionResponse)
def update_pothole_status(pothole_id: str, update: PotholeStatusUpdate, db: Session = Depends(get_db)):
    """Allows field officers or contractors to verify defects and update repair stages."""
    r = db.query(PotholeRecord).filter(PotholeRecord.pothole_id == pothole_id).first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Pothole {pothole_id} not found.")

    if update.verification_status is not None:
        r.verification_status = update.verification_status
    if update.repair_status is not None:
        r.repair_status = update.repair_status
    if update.severity is not None:
        r.severity = update.severity
        r.severity_reason = f"Human Verified & Re-classified: {r.severity_reason or ''}"

    db.commit()
    db.refresh(r)

    boxes = []
    if r.bounding_boxes_json:
        try:
            boxes = json.loads(r.bounding_boxes_json)
        except Exception:
            boxes = []

    return PotholeDetectionResponse(
        pothole_id=r.pothole_id,
        pothole_count=r.pothole_count,
        detections=boxes,
        avg_confidence=r.detection_confidence,
        severity=r.severity,
        severity_method=r.severity_method or "",
        severity_reason=r.severity_reason or "",
        image_url=r.image_path,
        annotated_image_url=r.annotated_image_path or r.image_path,
        latitude=r.latitude,
        longitude=r.longitude,
        road_name=r.road_name,
        state=r.state,
        verification_status=r.verification_status,
        repair_status=r.repair_status,
        model_id=r.model_id or "pothole-adapter-v1",
        processing_time_ms=r.processing_time_ms or 0.0,
        is_demo=bool(r.is_demo),
        detection_date=r.detection_date
    )


@router.post("/seed-samples")
def seed_pothole_samples(db: Session = Depends(get_db)):
    """Seeds audited demonstration pothole defects across major Indian corridors."""
    if db.query(PotholeRecord).count() >= 6:
        return {"message": "Sample pothole records already initialized.", "count": db.query(PotholeRecord).count()}

    samples = [
        {
            "pothole_id": "PH-2026-0001",
            "road_name": "NH-48 Pune-Bengaluru Km 142 (Khed Shivapur)",
            "state": "Maharashtra",
            "district": "Pune",
            "latitude": 18.3241,
            "longitude": 73.8612,
            "pothole_count": 2,
            "severity": "critical",
            "severity_method": "IRC Heuristic: Relative Frame Area & Multi-Defect Co-occurrence",
            "severity_reason": "High-priority hazard: 2 deep cavities spanning 9.4% of frame. Located in high-speed outer lane.",
            "detection_confidence": 0.88,
            "verification_status": "verified",
            "repair_status": "scheduled",
            "is_demo": True
        },
        {
            "pothole_id": "PH-2026-0002",
            "road_name": "NH-44 Outer Ring Road Corridor (Medchal)",
            "state": "Telangana",
            "district": "Hyderabad",
            "latitude": 17.6291,
            "longitude": 78.4812,
            "pothole_count": 1,
            "severity": "severe",
            "severity_method": "IRC Heuristic: Relative Frame Area & Multi-Defect Co-occurrence",
            "severity_reason": "Large asphalt crater spanning 5.8% of road perspective. High two-wheeler wobble risk.",
            "detection_confidence": 0.92,
            "verification_status": "verified",
            "repair_status": "in_progress",
            "is_demo": True
        },
        {
            "pothole_id": "PH-2026-0003",
            "road_name": "NH-19 Golden Quadrilateral (Varanasi Bypass)",
            "state": "Uttar Pradesh",
            "district": "Varanasi",
            "latitude": 25.3176,
            "longitude": 82.9739,
            "pothole_count": 3,
            "severity": "critical",
            "severity_method": "IRC Heuristic: Relative Frame Area & Multi-Defect Co-occurrence",
            "severity_reason": "Severe multi-defect cluster (3 co-located craters). Immediate cold-mix patch required.",
            "detection_confidence": 0.85,
            "verification_status": "verified",
            "repair_status": "reported",
            "is_demo": True
        },
        {
            "pothole_id": "PH-2026-0004",
            "road_name": "NH-66 Coastal Corridor (Panvel-Goa Highway Km 84)",
            "state": "Goa",
            "district": "North Goa",
            "latitude": 15.6021,
            "longitude": 73.8182,
            "pothole_count": 1,
            "severity": "moderate",
            "severity_method": "IRC Heuristic: Relative Frame Area & Multi-Defect Co-occurrence",
            "severity_reason": "Developing defect (2.8% of pavement area) aggravated by monsoon drainage runoff.",
            "detection_confidence": 0.79,
            "verification_status": "unverified",
            "repair_status": "reported",
            "is_demo": True
        },
        {
            "pothole_id": "PH-2026-0005",
            "road_name": "NH-48 Delhi-Jaipur Expressway (Manesar Flyover)",
            "state": "Haryana",
            "district": "Gurugram",
            "latitude": 28.3512,
            "longitude": 76.9382,
            "pothole_count": 1,
            "severity": "minor",
            "severity_method": "IRC Heuristic: Relative Frame Area & Multi-Defect Co-occurrence",
            "severity_reason": "Surface aggregate loss (1.2% frame area). Pavement seal coat scheduled.",
            "detection_confidence": 0.81,
            "verification_status": "verified",
            "repair_status": "repaired",
            "is_demo": True
        },
        {
            "pothole_id": "PH-2026-0006",
            "road_name": "GST Road (Chennai Suburban Corridor Km 28)",
            "state": "Tamil Nadu",
            "district": "Chengalpattu",
            "latitude": 12.8342,
            "longitude": 80.0431,
            "pothole_count": 2,
            "severity": "severe",
            "severity_method": "IRC Heuristic: Relative Frame Area & Multi-Defect Co-occurrence",
            "severity_reason": "Two craters (6.1% frame coverage) near high-traffic bus bay entrance.",
            "detection_confidence": 0.86,
            "verification_status": "verified",
            "repair_status": "scheduled",
            "is_demo": True
        }
    ]

    for s in samples:
        record = PotholeRecord(
            pothole_id=s["pothole_id"],
            image_path="/static/sample_pothole.jpg",
            annotated_image_path="/static/sample_pothole_annotated.jpg",
            latitude=s["latitude"],
            longitude=s["longitude"],
            road_name=s["road_name"],
            state=s["state"],
            district=s["district"],
            pothole_count=s["pothole_count"],
            bounding_boxes_json=json.dumps([{"box": [120, 240, 360, 420], "confidence": s["detection_confidence"], "label": "pothole", "relative_area": 0.05}]),
            detection_confidence=s["detection_confidence"],
            severity=s["severity"],
            severity_method=s["severity_method"],
            severity_reason=s["severity_reason"],
            verification_status=s["verification_status"],
            repair_status=s["repair_status"],
            reporter="NHAI Highway Audit Team",
            model_id="roadsafe-vision-adapter (audited)",
            processing_time_ms=42.5,
            is_demo=True
        )
        db.add(record)
    
    db.commit()
    return {"message": "Successfully seeded audited Indian highway blackspot potholes.", "count": len(samples)}
