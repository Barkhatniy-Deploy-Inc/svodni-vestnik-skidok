import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    """Проверка доступности корневого эндпоинта."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Добро пожаловать в API Сводного Вестника Скидок"}

@pytest.mark.asyncio
async def test_create_product(client: AsyncClient):
    """Тест создания товара (с моком парсера)."""
    # Мы пока не мокаем парсер на уровне кода, 
    # но проверим, что эндпоинт принимает данные и сохраняет их.
    payload = {
        "url": "https://www.ozon.ru/product/some-item/",
        "target_price": 1000.0
    }
    response = await client.post("/api/v1/products/", json=payload)
    
    # В тесте парсинг может упасть или вернуть "Неизвестный товар", 
    # это нормально для базового теста API.
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == payload["url"]
    assert data["target_price"] == payload["target_price"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_products(client: AsyncClient):
    """Тест получения списка товаров."""
    # Сначала добавим товар
    await client.post("/api/v1/products/", json={
        "url": "https://example.com/1",
        "target_price": 500
    })
    
    response = await client.get("/api/v1/products/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1
    assert items[0]["url"] == "https://example.com/1"
