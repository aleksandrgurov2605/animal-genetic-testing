from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, text, Float, func, and_, cast, case, Numeric

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_depends import get_async_db
from app.models import AnimalGeneticTests
from app.schemas import Statistics, HealthStatus

# Создаём маршрутизатор с префиксом и тегом
router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@router.get("/", response_model=list[Statistics])
async def get_statistics(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает статистику генетических тестов животных.
    """
    # textual_sql = text('''
    #                    SELECT species,
    #                           COUNT(*) AS total_tests,
    #                           ROUND((SUM(milk_yield) / COUNT(*)), 4) AS avg_milk_yield,
    #                           MAX(milk_yield) as max_milk_yield,
    #                           ROUND(CAST((
    #                                 SELECT COUNT(health_status)
    #                                 FROM animal_genetic_tests AS gt1
    #                                 WHERE health_status LIKE 'Здорова' AND gt1.species = animal_genetic_tests.species
    #                                 )
    #                           / (
    #                              SELECT COUNT(health_status)
    #                              FROM animal_genetic_tests AS gt2
    #                              WHERE gt2.species = animal_genetic_tests.species
    #                              ) AS numeric)
    #                          , 4) AS good_health_percentage
    #                    FROM animal_genetic_tests
    #                    GROUP BY species
    #                    ''')
    # statistics = await db.execute(textual_sql)

    stmt = (
        select(
            AnimalGeneticTests.species.label('species'),
            func.count().label('total_tests'),
            func.round(func.avg(cast(AnimalGeneticTests.milk_yield, Numeric)), 4).label('avg_milk_yield'),
            func.max(cast(AnimalGeneticTests.milk_yield, Numeric)).label('max_milk_yield'),
            func.round(
                cast(
                    (func.sum(
                        case((AnimalGeneticTests.health_status.like('Здорова'), 1), else_=0)) / func.count()) * 100,
                    Numeric
                ),
                4
            ).label('good_health_percentage')
        )
        .select_from(AnimalGeneticTests)
        .group_by(AnimalGeneticTests.species)
    )
    statistics = await db.execute(stmt)
    if not statistics:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no statistics'
        )
    return statistics.all()
