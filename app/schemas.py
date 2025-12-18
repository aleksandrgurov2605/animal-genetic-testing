from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class GeneticTest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'animal_name': 'Бурёнка',
                    'species': 'Корова',
                    'test_date': '2017-03-12',
                    'milk_yield': '22.4',
                    'health_status': 'Здорова'
                }
            ]
        }
    )
    animal_name: str
    species: str
    test_date: date
    milk_yield: str
    health_status: str

