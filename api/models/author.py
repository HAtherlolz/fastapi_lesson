from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from .base import Base
# from .course import Course


author_course_association = Table(
    'author_course', Base.metadata,
    Column('author_id', ForeignKey('authors.id', ondelete="CASCADE"), primary_key=True),
    Column('course_id', ForeignKey('courses.id', ondelete="CASCADE"), primary_key=True)
)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = Column(String(255))

    courses: Mapped[list["Course"]] = relationship(
        "Course",
        secondary=author_course_association,
        back_populates="authors",
        passive_deletes=True
    )



