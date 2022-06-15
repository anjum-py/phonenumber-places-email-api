from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import places, phonenumber, email, redis_db

description = """

### Phone numbers

- Lookup international codes for any country
- Format phone numbers

### Emails

- Verify domains using DNS lookups for any given email
- Normalize emails

### Places

- Lookup any place by city, state, country

### Timezone

- Lookup timezones for a given country

"""

tags_metadata = [
    {
        "name": "Places",
        "description": "Lookup cities, timezones, and basic info about countries",
    },
    {
        "name": "Validate Phone Numbers",
        "description": "Format and validate phone numbers",
    },
    {
        "name": "Validate Email",
        "description": "Format and validate emails",
    },
    {
        "name": "Redis DB",
        "description": "Operations related to Redis database.",
    },
]

fastapi_application = FastAPI(
    title="Phone number, email, and places API",
    description=description,
    version="0.1.0",
    terms_of_service="todo",
    contact={
        "name": "Mohammed Anjum",
        "url": "https://example.com",
        "email": "anjum@sahl.solutions",
    },
    license_info={
        "name": "todo",
        "url": "https://example.com",
    },
    openapi_tags=tags_metadata,
)

origins = [
    "http://localhost",
    "http://localhost:8000",
]


fastapi_application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


fastapi_application.include_router(places.router)
fastapi_application.include_router(phonenumber.router)
fastapi_application.include_router(email.router)
fastapi_application.include_router(redis_db.router)
