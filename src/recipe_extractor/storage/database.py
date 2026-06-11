from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from recipe_extractor.storage.models import Base


def get_engine(db_path: Path) -> Engine:
    db_path = db_path.resolve()
    return create_engine(f"sqlite:///{db_path}")


def create_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def get_session(engine: Engine) -> Session:
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()