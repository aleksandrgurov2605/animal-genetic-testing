from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, delete

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_depends import get_async_db
from app.models import AnimalGeneticTests
from app.schemas import GeneticTest, GeneticTestFromDB, AnimalSpecies

# Создаём маршрутизатор с префиксом и тегом
router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)


@router.get("/", response_model=list[GeneticTestFromDB])
async def get_all_animal_gts(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех генетических тестов животных.
    """
    result = await db.scalars(select(AnimalGeneticTests))
    animal_gts = result.all()
    return animal_gts


@router.get("/by_species", response_model=list[GeneticTestFromDB])
async def get_animal_by_species(species: str, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список генетических тестов животных определенного вида.
    """
    if species not in [species for species in AnimalSpecies]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Species not found. Доступные виды животных:" \
                                   f" {", ".join(species for species in AnimalSpecies)}")
    result = await db.scalars(select(AnimalGeneticTests).where(AnimalGeneticTests.species == species))
    animal_gts = result.all()
    return animal_gts


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_animal_gt(animal_gt: GeneticTest, db: AsyncSession = Depends(get_async_db)):
    """
    Создаёт новый генетический тест животного.
    """
    # Создание нового генетического теста животного
    db_animal_gt = AnimalGeneticTests(**animal_gt.model_dump())
    db.add(db_animal_gt)
    await db.commit()
    await db.refresh(db_animal_gt)
    return {
        "message": "Данные успешно добавлены",
        "id": db_animal_gt.id
    }


@router.put("/{animal_gt_id}", response_model=GeneticTest, status_code=status.HTTP_200_OK)
async def edit_animal_gt(
        animal_gt_id: int,
        animal_gt: GeneticTest,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Редактирует генетический тест животного.
    """
    result = await db.scalars(select(AnimalGeneticTests).where(AnimalGeneticTests.id == animal_gt_id))
    db_test_result = result.first()
    if not db_test_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genetic Test not found")

    await db.execute(
        update(AnimalGeneticTests).where(AnimalGeneticTests.id == animal_gt_id).values(**animal_gt.model_dump())
    )

    await db.commit()
    await db.refresh(db_test_result)
    return db_test_result


@router.delete("/{animal_gt_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_animal_gt(
        animal_gt_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Удаляет генетический тест животного.
    """
    result = await db.scalars(select(AnimalGeneticTests).where(AnimalGeneticTests.id == animal_gt_id))
    db_test_result = result.first()
    if not db_test_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Genetic Test not found")

    await db.execute(
        delete(AnimalGeneticTests).where(AnimalGeneticTests.id == animal_gt_id)
    )
    await db.commit()

    return {
        "message": "Данные успешно удалены",
        "id": animal_gt_id
    }

