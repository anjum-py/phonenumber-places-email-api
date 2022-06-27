from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from models import Email

router = APIRouter()

validate_email_responses = {
    "200" : {
        "model": Email,
        "description": "Returns formatted and normalized email, after making sure that associated domain is valid and has an MX record. However, cannot confirm email deliverability.",
        "detail": "Details about response",
        "content": {"application/json": {"example": {"email": "email@example.com"}}},
    },

    "422" : {
        "description": "Email is not valid and/or domain does not return an MX record",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/HTTPValidationError"
                }
            }
        },
    },
}


@router.get("/validate-email", responses=validate_email_responses, tags=["Validate Email"])
async def validate_email(email: str):
    """
    Returns valid email using [python-email-validator](https://github.com/JoshData/python-email-validator). Only checks if email has correct syntax and MX record exists for domain.
    \n
    Please note that checking DNS records might take a couple of seconds.
    """
    try:
        return Email(email=email)
    except ValidationError as e:
        return JSONResponse(status_code=422, content=e.errors())
