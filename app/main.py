from fastapi import FastAPI

from app.routers.animal_genetic_tests import router as animal_gts_router
from app.routers.statistics import router as statistics_router
from app.routers.users import router as users_router

app = FastAPI(
    title="Animal Genetic Testing",
)


@app.get("/")
async def root():
    return {"message": f"Добро пожаловать в API Animal Genetic Testing!"}


app.include_router(animal_gts_router)
app.include_router(statistics_router)
app.include_router(users_router)
