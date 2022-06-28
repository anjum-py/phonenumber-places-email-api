import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import places, phonenumber, email, redis_db

description = """

### Phone numbers

- Lookup international codes for any country
- Regional formatting for phone numbers.

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

app = FastAPI(
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

origins = os.getenv("CORS_ORIGINS", "").split()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(places.router)
app.include_router(phonenumber.router)
app.include_router(email.router)
app.include_router(redis_db.router)
