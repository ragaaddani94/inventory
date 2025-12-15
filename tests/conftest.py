import sys
import os
# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    await app.router.startup()
    try:
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    finally:
        await app.router.shutdown()

@pytest.fixture
def headers():
    return {"X-Client-Source": "test"}