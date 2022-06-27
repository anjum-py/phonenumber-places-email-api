import os
import redis.asyncio as redis
from redis.exceptions import ConnectionError, ResponseError
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

redis_host: str = os.getenv("REDIS_HOST", "localhost")
redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
connection: redis.Redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


class RedisIndex:
    """
    Base class for managing indexes
    
    """
    def __init__(self) -> None:
        self.schema = self.schema
        self.name = self.name
        self.prefix = self.prefix
        self.definition = IndexDefinition(
            prefix=[self.prefix],
            index_type=IndexType.HASH,
        )

    def get_field_names(self) -> list:
        """
        Does not return "as_name"
        At the moment, no field is implemented with as_name
        """
        fields = []
        for s in self.schema:
            fields.append(s.name)
        return fields

    async def index_exists(self) -> bool:
        """
        Checks and creates redis index if not already present
        """
        try:
            await connection.ft(index_name=self.name).info()
            return True
        except ResponseError:
            await connection.ft(index_name=self.name).create_index(
                self.schema,
                definition=self.definition,
            )
            return True
        except ConnectionError:
            return False

    async def search(self, qs: str, query_type: str) -> list:
        """
        """

        fields: list = self.get_field_names()
        q: Query = Query(f"{qs}")

        if query_type == "wildcard":
            q = Query(f"{qs}*")
        if query_type == "fuzzy":
            q = Query(f"%{qs}%")

        r = await connection.ft(self.name).search(q)

        d = [{field: getattr(doc, field) for field in fields} for doc in r.docs]

        result = {
            "total" : r.total,
            "duration" : r.duration,
            "records" : d,
        }

        return result


class CountryIndex(RedisIndex):

    schema = (
        TextField("id"),
        TextField("name"),
        TextField("iso3"),
        TextField("iso2"),
        TextField("phone_code"),
        TextField("numeric_code"),
        TextField("capital"),
        TextField("currency"),
        TextField("currency_name"),
        TextField("currency_symbol"),
        TextField("tld"),
        TextField("native"),
        TextField("region"),
        TextField("subregion"),
        TextField("emoji"),
        TextField("emojiU"),
        TextField("latitude"),
        TextField("longitude"),
    )

    name = "countries"
    prefix = "country:"


class TimeZoneIndex(RedisIndex):

    schema = (
        TextField("id"),
        TextField("zone_name"),
        TextField("gmt_offset"),
        TextField("gmt_offset_name"),
        TextField("abbreviation"),
        TextField("tz_name"),
        TextField("country_id"),
        TextField("country_name"),
        TextField("emoji"),
    )

    name = "timezones"
    prefix = "timezone:"


class StateIndex(RedisIndex):

    schema = (
        NumericField("id"),
        TextField("name"),
        TextField("country_id"),
        TextField("country_code"),
        TextField("country_name"),
        TextField("state_code"),
        TextField("type"),
        TextField("latitude"),
        TextField("longitude"),
    )

    name = "states"
    prefix = "state:"


class CityIndex(RedisIndex):

    schema = (
        NumericField("id"),
        TextField("name"),
        TextField("state_id"),
        TextField("state_code"),
        TextField("state_name"),
        TextField("country_id"),
        TextField("country_code"),
        TextField("country_name"),
        TextField("latitude"),
        TextField("longitude"),
    )

    name = "cities"
    prefix = "city:"

