import pytest

@pytest.mark.asyncio
async def test_create_product(client, headers):
    response = await client.post(
        "/v1/products",
        json={
            "sku": "TEST-123",
            "name": "Test Product",
            "price": 29.99,
            "currency": "USD"
        },
        headers=headers
    )
    assert response.status_code in [201, 409]

@pytest.mark.asyncio
async def test_get_product(client, headers):
    response = await client.get(
        "/v1/products/TEST-123",
        headers=headers
    )
    assert response.status_code in [200, 404]