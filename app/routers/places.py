from fastapi import APIRouter
from enum import Enum
from db.indexes import CountryIndex, TimeZoneIndex, CityIndex
from models import CountrySearch, TimeZoneSearch, CitySearch

router = APIRouter()

class QueryType(str, Enum):
    fuzzy = "fuzzy"
    wildcard = "wildcard"
    exact = "exact"

country_lookup_responses = {
    200: {
        "model": CountrySearch,
        "description": "Returns a list of matched countries for given query",
        "content": {
            "application/json": {
                "example": {
                    "total": "1",
                    "duration": "5",
                    "records": [
                        {
                            "id": "country:101",
                            "name": "India",
                            "iso3": "IND",
                            "iso2": "IN",
                            "numeric_code": "356",
                            "phone_code": "91",
                            "capital": "New Delhi",
                            "currency": "INR",
                            "currency_name": "Indian rupee",
                            "currency_symbol": "₹",
                            "tld": ".in",
                            "native": "भारत",
                            "region": "Asia",
                            "subregion": "Southern Asia",
                            "latitude": "20.00000000",
                            "longitude": "77.00000000",
                            "emoji": "🇮🇳",
                            "emojiU": "U+1F1EE U+1F1F3",
                        }
                    ],
                }
            }
        },
    }
}


@router.get("/country-lookup", responses=country_lookup_responses, tags=["Places"])
async def country_lookup(
    query: str,
    query_type: QueryType,
):
    """
    Lookup basic details about any country.
    \n
    Select the type of search:
    \n
    "exact" = Will return documents that match the input exactly
    \n
    "wildcard" = Will return documents that match **"input*"**
    \n
    "fuzzy" = Will return documents that match for **"%input%"**
    \n
    Search in any field.
    """

    r = await CountryIndex().search(query, query_type)
    return CountrySearch(**r)


timezone_lookup_responses = {
    200: {
        "model": TimeZoneSearch,
        "description": "Returns a list of matched timezone records for given query",
        "content": {
            "application/json": {
                "example": {
                    "total": "1",
                    "duration": "2.447366714477539",
                    "records": [
                        {
                            "zone_name": "Asia/Kolkata",
                            "gmt_offset": "19800",
                            "gmt_offset_name": "UTC+05:30",
                            "abbreviation": "IST",
                            "tz_name": "Indian Standard Time",
                            "country_id": 101,
                            "country_name": "India",
                        }
                    ],
                }
            }
        },
    }
}


@router.get("/timezone-lookup", responses=timezone_lookup_responses, tags=["Places"])
async def timezone_lookup(
    query: str,
    query_type: QueryType,
):
    """
    Lookup timezone by country or timezone name.
    \n
    Select the type of search:
    \n
    "exact" = Will return documents that match the input exactly
    \n
    "wildcard" = Will return documents that match **"input*"**
    \n
    "fuzzy" = Will return documents that match for **"%input%"**
    \n
    Search in any field.
    """

    r = await TimeZoneIndex().search(query, query_type)
    return TimeZoneSearch(**r)


place_lookup_responses = {
    200: {
        "model": CitySearch,
        "description": "Returns a list of matched cities records for given query",
        "content": {
            "application/json": {
                "example": {
                    "total": "1",
                    "duration": "1.6524791717529297",
                    "records": [
                        {
                            "id": "city:57847:state:4026:country:101",
                            "name": "Bangalore Rural",
                            "state_id": "4026",
                            "state_code": "KA",
                            "state_name": "Karnataka",
                            "country_id": "101",
                            "country_code": "IN",
                            "country_name": "India",
                            "latitude": "13.22567000",
                            "longitude": "77.57501000",
                        }
                    ],
                }
            }
        },
    }
}


@router.get("/place-lookup", responses=place_lookup_responses, tags=["Places"])
async def place_lookup(
    query: str,
    query_type: QueryType,
):
    """
    Lookup cities or states by country, state, or cities.
    \n
    Select the type of search:
    \n
    "exact" = Will return documents that match the input exactly
    \n
    "wildcard" = Will return documents that match **"input*"**
    \n
    "fuzzy" = Will return documents that match for **"%input%"**
    \n
    Search in any field.
    """

    r = await CityIndex().search(query, query_type)
    return CitySearch(**r)
