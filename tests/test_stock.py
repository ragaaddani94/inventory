import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_adjust_stock(client):
    # Adjust stock
    response = await client.post(
            "/v1/stock/adjust",
            json={
                "sku": "STOCK-TEST",
                "delta": 5,
                "transactionId": "test-tx-1"
            },
            headers={"X-Client-Source": "test"}
        )
    # Even if product doesn't exist, it should still work (upsert)
    assert response.status_code == 200
    data = response.json()
    assert "sku" in data
    assert "newQuantity" in data

@pytest.mark.asyncio
async def test_adjust_stock_idempotent(client):
    # Same request twice
    data = {
        "sku": "IDEMPOTENT-TEST",
        "delta": 3,
        "transactionId": "same-tx-id"
    }
    
    # First request
    response1 = await client.post(
        "/v1/stock/adjust",
        json=data,
        headers={"X-Client-Source": "test"}
    )
    
    # Second identical request
    response2 = await client.post(
        "/v1/stock/adjust",
        json=data,
        headers={"X-Client-Source": "test"}
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    # Both should return the same quantity
    assert response1.json()["newQuantity"] == response2.json()["newQuantity"]