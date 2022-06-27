from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError
from unittest.mock import patch
from routers.redis_db import build_db_info
from main import fastapi_application

client = TestClient(fastapi_application)

valid_db_result = {
    "uptime_in_seconds": 651,
    "uptime_in_days": 0,
    "memory_in_use": "166.82M",
    "total_keys": 148947,
    "total_indexes": 3,
    "index_info": [
        {
            "index_name": "cities",
            "number_of_records": 148266,
            "last_updated": "a day",
        },
        {
            "index_name": "countries",
            "number_of_records": 250,
            "last_updated": "a day",
        },
        {
            "index_name": "timezones",
            "number_of_records": 428,
            "last_updated": "a day",
        },
    ],
}

@patch('routers.redis_db.build_db_info')
def test_get_redis_db_info(mocked):
    mocked.return_value = valid_db_result
    response = client.get("/redis-db-info")
    assert response.status_code == 200, "Should return a valid response code, 200"


@patch('routers.redis_db.build_db_info')
def test_get_redis_db_connection_error(mocked):
    mocked.side_effect = ConnectionError
    response = client.get("/redis-db-info")
    assert response.status_code == 500, "Should return 500 for redis connection error"
