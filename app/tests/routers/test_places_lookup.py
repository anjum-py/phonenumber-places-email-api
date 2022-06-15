from fastapi.testclient import TestClient
from unittest.mock import patch
from models.models import Country
from routers.places import CountryIndex, TimeZoneIndex, CityIndex
from main import fastapi_application

client = TestClient(fastapi_application)

get_country_result = {
    "total": "1",
    "duration": "4.789590835571289",
    "records": [
        {
            "id": "country:32",
            "name": "British Indian Ocean Territory",
            "iso3": "IOT",
            "iso2": "IO",
            "numeric_code": "086",
            "phone_code": "246",
            "capital": "Diego Garcia",
            "currency": "USD",
            "currency_name": "United States dollar",
            "currency_symbol": "$",
            "tld": ".io",
            "native": "British Indian Ocean Territory",
            "region": "Africa",
            "subregion": "Eastern Africa",
            "latitude": "-6.00000000",
            "longitude": "71.50000000",
            "emoji": "🇮🇴",
            "emojiU": "U+1F1EE U+1F1F4",
        }
    ],
}


@patch.object(CountryIndex, "search", return_value=get_country_result, spec=True)
def test_get_country_lookup(mocked):
    response = client.get(
        "/country-lookup", params={"query": "british", "query_type": "fuzzy"}
    )
    assert mocked.assert_called_once, "Should have been called once"
    assert response.status_code == 200, "Should return a valid response code, 200"


def test_get_country_422():
    response = client.get("/country-lookup", params={"query": "british"})
    assert response.status_code == 422, "Should return 422 for missing query parameters"


get_timezone_result = {
    "total": "32",
    "duration": "19.797325134277344",
    "records": [
        {
            "zone_name": "America/Adak",
            "gmt_offset": "-36000",
            "gmt_offset_name": "UTC-10:00",
            "abbreviation": "HST",
            "tz_name": "Hawaii\\u2013Aleutian Standard Time",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Anchorage",
            "gmt_offset": "-32400",
            "gmt_offset_name": "UTC-09:00",
            "abbreviation": "AKST",
            "tz_name": "Alaska Standard Time",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Boise",
            "gmt_offset": "-25200",
            "gmt_offset_name": "UTC-07:00",
            "abbreviation": "MST",
            "tz_name": "Mountain Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Chicago",
            "gmt_offset": "-21600",
            "gmt_offset_name": "UTC-06:00",
            "abbreviation": "CST",
            "tz_name": "Central Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Denver",
            "gmt_offset": "-25200",
            "gmt_offset_name": "UTC-07:00",
            "abbreviation": "MST",
            "tz_name": "Mountain Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Detroit",
            "gmt_offset": "-18000",
            "gmt_offset_name": "UTC-05:00",
            "abbreviation": "EST",
            "tz_name": "Eastern Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Indiana/Indianapolis",
            "gmt_offset": "-18000",
            "gmt_offset_name": "UTC-05:00",
            "abbreviation": "EST",
            "tz_name": "Eastern Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Indiana/Knox",
            "gmt_offset": "-21600",
            "gmt_offset_name": "UTC-06:00",
            "abbreviation": "CST",
            "tz_name": "Central Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Indiana/Marengo",
            "gmt_offset": "-18000",
            "gmt_offset_name": "UTC-05:00",
            "abbreviation": "EST",
            "tz_name": "Eastern Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
        {
            "zone_name": "America/Indiana/Petersburg",
            "gmt_offset": "-18000",
            "gmt_offset_name": "UTC-05:00",
            "abbreviation": "EST",
            "tz_name": "Eastern Standard Time ",
            "country_id": 233,
            "country_name": "United States",
        },
    ],
}


@patch.object(TimeZoneIndex, "search", return_value=get_timezone_result, spec=True)
def test_get_timezone(mocked):
    response = client.get(
        "/timezone-lookup", params={"query": "state", "query_type": "exact"}
    )
    assert mocked.assert_called_once, "Should have been called once"
    assert response.status_code == 200, "Should return a valid response code, 200"


def test_get_timezone_422():
    response = client.get("/timezone-lookup", params={"query": "states"})
    assert response.status_code == 422, "Should return 422 for missing query parameters"


get_place_result = {
    "total": "1",
    "duration": "2.1851062774658203",
    "records": [
        {
            "id": "city:57933:state:4026:country:101",
            "name": "Bengaluru",
            "state_id": "4026",
            "state_code": "KA",
            "state_name": "Karnataka",
            "country_id": "101",
            "country_code": "IN",
            "country_name": "India",
            "latitude": "12.97194000",
            "longitude": "77.59369000",
        }
    ],
}


@patch.object(CityIndex, "search", return_value=get_place_result, spec=True)
def test_get_places(mocked):
    response = client.get(
        "/place-lookup", params={"query": "bengaluru", "query_type": "exact"}
    )
    assert mocked.assert_called_once, "Should have been called once"
    assert response.status_code == 200, "Should return a valid response code, 200"


def test_get_places_422():
    response = client.get("/place-lookup", params={"query": "bengaluru"})
    assert response.status_code == 422, "Should return 422 for missing query parameters"
