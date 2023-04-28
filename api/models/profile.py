from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, declarative_base

Base = declarative_base()


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    avatar: Mapped[str] = Column(String(255), nullable=True)
    email: Mapped[str] = Column(String(55), unique=True, nullable=False, index=True)
    password: Mapped[str] = Column(String, nullable=False)
    first_name: Mapped[str] = Column(String(30), nullable=True)
    last_name: Mapped[str] = Column(String(30), nullable=True)

    lat: Mapped[float] = Column(Float)
    lng: Mapped[float] = Column(Float)

    country: Mapped[str] = Column(String)
    city: Mapped[str] = Column(String)

    date_joined: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
