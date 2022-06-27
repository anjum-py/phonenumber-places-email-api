from email_validator import validate_email
from pydantic import BaseModel, create_model, EmailStr
from typing import List, Optional, Union


class EmailDomainCheck(EmailStr):
    @classmethod
    def validate(cls, value: Union[str]) -> str:
        value = value.replace(" ", "").lower()
        return validate_email(value)["email"]


class Docs(BaseModel):
    index_name: Optional[str] = ""
    number_of_records: Optional[int] = 0
    last_updated: Optional[str] = 0


class RedisInfo(BaseModel):
    uptime_in_seconds: Optional[int]
    uptime_in_days: Optional[int]
    memory_in_use: Optional[str]
    total_keys: Optional[int]
    total_indexes: Optional[int]
    index_info: List[Docs]


class TimeZone(BaseModel):
    id: Optional[str]
    zone_name: Optional[str]
    gmt_offset: Optional[str]
    gmt_offset_name: Optional[str]
    abbreviation: Optional[str]
    tz_name: Optional[str]
    country_id: Optional[int]
    country_name: Optional[str]
    emoji: Optional[str]


class TimeZoneSearch(BaseModel):
    total: str
    duration: str
    records: List[TimeZone]


class Country(BaseModel):

    id: str
    name: str
    iso3: str
    iso2: str
    numeric_code: Optional[str]
    phone_code: str
    capital: str
    currency: str
    currency_name: str
    currency_symbol: str
    tld: str
    native: str
    region: str
    subregion: str
    latitude: str
    longitude: str
    emoji: Optional[str]
    emojiU: Optional[str]


class CountrySearch(BaseModel):
    total: str
    duration: str
    records: List[Country]


class State(BaseModel):

    id: str
    name: str
    country_id: str
    country_code: str
    country_name: str
    state_code: str
    type: str
    latitude: str
    longitude: str


class City(BaseModel):

    id: str
    name: str
    state_id: str
    state_code: str
    state_name: str
    country_id: str
    country_code: str
    country_name: str
    latitude: str
    longitude: str


class CitySearch(BaseModel):
    total: str
    duration: str
    records: List[City]


class PhoneNumber(BaseModel):
    is_valid_number: Optional[bool] = False
    national_format: Optional[str]
    international_format: Optional[str]
    e164_format: Optional[str]


class Email(BaseModel):
    email: EmailDomainCheck
