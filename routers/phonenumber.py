import phonenumbers
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Query
from models import PhoneNumber
from fastapi.responses import JSONResponse

router = APIRouter()


validate_phone_responses = {
    "200": {
        "model": PhoneNumber,
        "description": "Returns validated phone number in various formats, using [python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers), based on **libphonenumber** by Google",
        "content": {
            "application/json": {
                "example": {
                    "is_valid_number": True,
                    "national_format": "(234) 567-8999",
                    "international_format": "+1 234-567-8999",
                    "e164_format": "+12345678999",
                }
            },
        },
    }
}


@router.get(
    "/validate-phone-numbers",
    responses=validate_phone_responses,
    tags=["Validate Phone Numbers"],
)
async def validate_phone_numbers(
    phone_number: str,
    country_code: str = Query(
        None, description="Two-letter iso2 code of country, e.g., 'IN' for India"
    ),
):

    try:
        number = phonenumbers.parse(phone_number, country_code)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return JSONResponse(
            status_code=422, content=jsonable_encoder({"detail": e._msg})
        )

    result = {
        "is_valid_number": phonenumbers.is_valid_number(number),
        "national_format": phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.NATIONAL
        ),
        "international_format": phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
        "e164_format": phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.E164
        ),
    }

    return PhoneNumber(**result)
