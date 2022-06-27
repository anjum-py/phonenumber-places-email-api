from redis.exceptions import ConnectionError
from unittest.mock import patch
from db.async_db import ManageCountries

@patch.object(ManageCountries, 'download_file', return_value = None)
@patch.object(ManageCountries, 'update_db', return_value = None)
def test_redis_key(mocked):
    d = ManageCountries().download_file()
    assert not d

@patch.object(ManageCountries, 'update_db', return_value = None)
async def test_redis_key(mocked):
    d = await ManageCountries().download_file()
    assert not d
