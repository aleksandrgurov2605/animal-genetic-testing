from httpx import AsyncClient


async def test_create_user_success(async_client: AsyncClient):
    response = await async_client.post(
        "/users/", json={"email": "test_email@test.com", "password": "password"}
    )
    assert response.status_code == 201


async def test_create_user_unsuccess(async_client: AsyncClient):
    response = await async_client.post(
        "/users/", json={"email": "test_email@test.com", "password": "password"}
    )
    assert response.status_code == 400


async def test_create_user_unsuccess_2(async_client: AsyncClient):
    response = await async_client.post(
        "/users/", json={"email": "test_email_2@test.com", "password": "pas"}
    )
    assert response.status_code == 422
    assert response.json().get("detail") == [
        {
            "type": "string_too_short",
            "loc": ["body", "password"],
            "msg": "String should have at least 8 characters",
            "input": "pas",
            "ctx": {"min_length": 8},
        }
    ]


async def test_login_success(async_client: AsyncClient):
    response_create = await async_client.post(
        "/users/",
        json={"email": "test_email_for_login@test.com", "password": "password"},
    )
    assert response_create.status_code == 201
    response = await async_client.post(
        "/users/token",
        data={"username": "test_email_for_login@test.com", "password": "password"},
    )
    assert response.status_code == 200
    assert len(response.json().get("access_token")) == 195
