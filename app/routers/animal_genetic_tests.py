from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_depends import get_async_db
from app.models import AnimalGeneticTests
from app.schemas import GeneticTest

# Создаём маршрутизатор с префиксом и тегом
router = APIRouter(
    prefix="/animal_genetic_tests",
    tags=["animal_genetic_tests"],
)


@router.get("/", response_model=list[GeneticTest])
async def get_all_animal_gts(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех генетических тестов животных.
    """
    result = await db.scalars(select(AnimalGeneticTests))
    animal_gts = result.all()
    return animal_gts


@router.post("/", response_model=GeneticTest, status_code=status.HTTP_201_CREATED)
async def create_animal_gt(animal_gt: GeneticTest, db: AsyncSession = Depends(get_async_db)):
    """
    Создаёт новый генетический тест животного.
    """
    # Создание нового генетического теста животного
    # db_animal_gt = AnimalGeneticTests(**animal_gt.model_dump())
    db_animal_gt = AnimalGeneticTests(id=1, **animal_gt.model_dump())
    db.add(db_animal_gt)
    await db.commit()
    await db.refresh(db_animal_gt)
    return db_animal_gt
