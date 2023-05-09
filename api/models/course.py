from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, relationship

from .base import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = Column(String(255))

    lessons: Mapped["Course"] = relationship(
        "Lesson", back_populates="course"
    )

    authors: Mapped[list["Author"]] = relationship(
        "Author",
        secondary="author_course",
        back_populates="courses",
        passive_deletes=True
    )
