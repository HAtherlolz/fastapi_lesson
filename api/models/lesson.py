from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column("name", String(255))
    course_id: Mapped[int] = mapped_column("course_id", ForeignKey("courses.id", ondelete="CASCADE"))

    course: Mapped["Course"] = relationship(
        "Course", back_populates="lessons"
    )
