from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class HealthStatus(str, Enum):
    GOOD = "Здорова"
    BAD = "Больна"


class AnimalSpecies(str, Enum):
    cow = "Корова"
    goat = "Коза"
    sheep = "Овца"


class GeneticTest(BaseModel):
    animal_name: str = Field(min_length=2, max_length=30, description="Имя животного")
    species: AnimalSpecies = Field(description="Вид животного: Корова, Овца, Коза")
    test_date: date = Field(description="Дата проведения генетического теста животного")
    milk_yield: float = Field(
        ge=0, lt=50, description="Продуктивность животного в литрах"
    )
    health_status: HealthStatus = Field(
        description="Состояние здоровья животного: Здорова, Больна"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "animal_name": "Бурёнка",
                    "species": "Корова",
                    "test_date": "2017-03-12",
                    "milk_yield": "22.4",
                    "health_status": "Здорова",
                }
            ]
        }
    )


class GeneticTestFromDB(BaseModel):
    id: int
    animal_name: str
    species: AnimalSpecies
    test_date: date
    milk_yield: float
    health_status: HealthStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Statistics(BaseModel):
    species: str = Field(description="Вид животного: Корова, Овца, Коза")
    total_tests: int = Field(description="Количество тестов для данного вида животного")
    avg_milk_yield: float = Field(
        description="Среднее значение продуктивности для данного вида животного"
    )
    max_milk_yield: float = Field(
        description="Максимальное значение продуктивности для данного вида животного"
    )
    good_health_percentage: float = Field(
        description="Процент животных данного вида с хорошим состоянием здоровья"
    )


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"email": "user@example.com", "password": "stringst"}]
        }
    )


class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    refresh_token: str
