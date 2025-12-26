from httpx import AsyncClient

correct_data_for_post_test = {
    "animal_name": "Бурёнка",
    "health_status": "Здорова",
    "milk_yield": 22.4,
    "species": "Корова",
    "test_date": "2017-03-12"
}

correct_data_for_put_test = {
    "animal_name": "Бурёнка_Edit_version",
    "health_status": "Здорова",
    "milk_yield": 12,
    "species": "Корова",
    "test_date": "2017-03-12"
}
incorrect_data_for_post_test = {
    "animal_name": "Бурёнка",
    "health_status": "Здорова",
    "milk_yield": 22.4,
    "species": "Бык",
    "test_date": "2017-03-12"
}

stats = [{'species': 'Овца', 'total_tests': 1, 'avg_milk_yield': 4.0, 'max_milk_yield': 4.0,
          'good_health_percentage': 100.0},
         {'species': 'Коза', 'total_tests': 1, 'avg_milk_yield': 2.0, 'max_milk_yield': 2.0,
          'good_health_percentage': 0.0},
         {'species': 'Корова', 'total_tests': 7, 'avg_milk_yield': 16.6286, 'max_milk_yield': 22.4,
          'good_health_percentage': 85.7143}]


async def test_welcome(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"message": f"Hello World!"}
    assert response.headers["content-type"] == "application/json"


async def test_get_all_animal_gts(async_client: AsyncClient):
    response = await async_client.get("/tests/")
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.headers["content-type"] == "application/json"


async def test_get_animal_by_species_success(async_client: AsyncClient):
    response = await async_client.get("/tests/by_species?species=Корова")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.headers["content-type"] == "application/json"


async def test_get_animal_by_species_not_found(async_client: AsyncClient):
    response = await async_client.get("/tests/by_species?species=ороваf")
    assert response.status_code == 404
    assert response.json() == {"detail": "Species not found. Доступные виды животных: Корова, Коза, Овца"}
    assert "application/json" in response.headers["content-type"]


async def test_create_animal_gt_success(async_client: AsyncClient):
    response = await async_client.post("/tests/", json=correct_data_for_post_test)
    assert response.status_code == 201
    assert response.json()["message"] == "Данные успешно добавлены"
    assert "application/json" in response.headers["content-type"]


async def test_create_animal_gt_unsuccess(async_client: AsyncClient):
    response = await async_client.post("/tests/", json=incorrect_data_for_post_test)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be 'Корова', 'Коза' or 'Овца'"
    assert "application/json" in response.headers["content-type"]


async def test_edit_animal_gt_success(async_client: AsyncClient):
    response = await async_client.post("/tests/", json=correct_data_for_post_test)
    assert response.status_code == 201
    created = response.json()
    put_response = await async_client.put(f"/tests/{created['id']}", json=correct_data_for_put_test)
    assert put_response.status_code == 200
    updated = put_response.json()
    assert updated["animal_name"] == "Бурёнка_Edit_version"
    assert updated["milk_yield"] == 12


async def test_edit_animal_gt_unsuccess(async_client: AsyncClient):
    response = await async_client.post("/tests/", json=correct_data_for_post_test)
    assert response.status_code == 201
    created = response.json()
    put_response = await async_client.put(f"/tests/{created['id']}", json=incorrect_data_for_post_test)
    assert put_response.status_code == 422
    updated = put_response.json()
    assert updated["detail"][0]["msg"] == "Input should be 'Корова', 'Коза' or 'Овца'"


async def test_delete_animal_gt_success(async_client: AsyncClient):
    response = await async_client.post("/tests/", json=correct_data_for_post_test)
    assert response.status_code == 201
    created = response.json()
    put_response = await async_client.delete(f"/tests/{created['id']}")
    assert put_response.status_code == 200
    deleted = put_response.json()
    assert deleted["message"] == "Данные успешно удалены"
    assert deleted["id"] == created['id']


async def test_delete_animal_gt_unsuccess(async_client: AsyncClient):
    response = await async_client.post("/tests/", json=correct_data_for_post_test)
    assert response.status_code == 201
    created = response.json()
    put_response = await async_client.delete(f"/tests/{created['id'] + 100}")
    assert put_response.status_code == 404
    deleted = put_response.json()
    assert deleted["detail"] == "Genetic Test not found"


async def test_get_statistics_success(async_client: AsyncClient):
    response = await async_client.get("/statistics/")
    assert response.status_code == 200
    assert response.json() == stats


