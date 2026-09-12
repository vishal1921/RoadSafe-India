from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import settings

def resolve_db_url(url: str) -> str:
    """Ensure SQLite database URL points to an absolute project path regardless of current working directory."""
    if url.startswith("sqlite:///"):
        path_part = url[len("sqlite:///"):]
        p = Path(path_part)
        if not p.is_absolute():
            base_dir = Path(__file__).resolve().parent.parent
            clean_part = path_part.lstrip("./\\")
            abs_db_file = (base_dir / clean_part).resolve()
            return f"sqlite:///{abs_db_file.as_posix()}"
    return url

db_url = resolve_db_url(settings.DATABASE_URL)

# Create database engine
engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {},
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
