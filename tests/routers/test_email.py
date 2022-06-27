from fastapi.testclient import TestClient
from main import fastapi_application

client = TestClient(fastapi_application)

valid_email_result = {"email": "anjum@sahl.solutions"}


def test_get_validate_email():
    response = client.get("/validate-email", params={"email": "anjum@sahl.solutions"})
    assert response.status_code == 200, "Should return a valid response code, 200"


def test_get_validate_phone_number_422():
    response = client.get("/validate-email", params={"email": ""})
    assert response.status_code == 422, "Should return 422 for missing email input"

