from fastapi import FastAPI

from app.routers.animal_genetic_tests import router as animal_gts_router
from app.routers.statistics import router as statistics_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"Hello World!"}


app.include_router(animal_gts_router)
app.include_router(statistics_router)
