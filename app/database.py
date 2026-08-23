from datetime import datetime
from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from app.config import get_settings


class Base(DeclarativeBase):
    pass


class TrafficStateRecord(Base):
    __tablename__ = "traffic_states"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    payload: Mapped[str] = mapped_column(String)


class StrategyRecord(Base):
    __tablename__ = "strategies"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    payload: Mapped[str] = mapped_column(String)


def make_engine(url: str | None = None):
    return create_engine(url or get_settings().database_url, connect_args={"check_same_thread": False} if (url or get_settings().database_url).startswith("sqlite") else {})


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(engine)

