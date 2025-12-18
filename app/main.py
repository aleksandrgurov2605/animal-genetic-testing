from fastapi import FastAPI

from app.core.config import settings
from app.routers.animal_genetic_tests import router as animal_gts_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"Hello World! {settings.ASYNC_DATABASE_URL}"}


app.include_router(animal_gts_router)