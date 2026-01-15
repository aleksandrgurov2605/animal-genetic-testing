import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class AnimalGeneticTests(Base):
    __tablename__ = "animal_genetic_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    animal_name: Mapped[str]
    species: Mapped[str]
    test_date: Mapped[datetime.date]
    milk_yield: Mapped[float]
    health_status: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="tests")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    tests: Mapped[list["AnimalGeneticTests"]] = relationship(
        "AnimalGeneticTests", back_populates="user"
    )
