import datetime

from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AnimalGeneticTests(Base):
    __tablename__ = "animal_genetic_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    animal_name: Mapped[str]
    species: Mapped[str]
    test_date: Mapped[datetime.date]
    milk_yield: Mapped[float]
    health_status: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
