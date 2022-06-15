valid_number_result = {
  "is_valid_number": False,
  "national_format": "1234567899",
  "international_format": "+1 1234567899",
  "e164_format": "+11234567899"
}

from fastapi.testclient import TestClient
from main import fastapi_application

client = TestClient(fastapi_application)

valid_email_result = {"email": "anjum@sahl.solutions"}


def test_get_validate_phone_number():
    response = client.get("/validate-phone-numbers", params={"phone_number": "1234567899", "country_code":"US"})
    assert response.status_code == 200, "Should return a valid response code, 200"


def test_get_validate_phone_number_422():
    response = client.get("/validate-phone-numbers", params={"phone_number": "1234567899"})
    assert response.status_code == 422, "Should return 422 for missing email input"

