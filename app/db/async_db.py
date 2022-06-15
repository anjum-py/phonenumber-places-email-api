import csv, re, os, time, aiohttp, aiofiles, datetime, humanize
from typing import Optional
from redis.asyncio.client import Redis
from models import (
    Country,
    City,
    State,
    TimeZone,
)
from db.indexes import (
    CountryIndex,
    TimeZoneIndex,
    CityIndex,
    StateIndex,
    connection,
)

class WithinSetTime(Exception):
    """
    Exception raised when set time limit for duration between updates is still valid.
    """

    def __init__(self):
        self.message = f"""

    Set interval for database updates has not elapsed
    Countries data usually does not get updated very often

    You can force update by using "python manage.py populate-db --force"

        """
        super().__init__(self.message)


class RedisDBBase:
    pipeline: Redis = connection.pipeline()
    base_dir: str = "/src/app/downloads/"
    update_interval: int = 15 * 24 * 60 * 60  # 15 days in seconds
    max_allowed_commands: int = 10000

    async def update_db_info(self, pipe: Redis = None) -> Optional[Redis]:
        key: str = f"dbinfo:{self.index.name.lower()}"
        base_value: dict = {"last_updated": int(time.time())}
        if pipe:
            return await pipe.hmset(key, mapping=base_value)
        else:
            return await connection.hmset(key, mapping=base_value)

    async def set_time_has_lapsed(self) -> bool:
        timestamp: list = await connection.hmget(
            f"dbinfo:{self.index.name.lower()}", "last_updated"
        )
        now = int(time.time())
        updated_on: int = (
            int(timestamp[0]) if timestamp[0] else (now - self.update_interval - 100)
        )
        lapsed: int = now - updated_on

        if lapsed > self.update_interval:
            return True
        return False

    async def reset_elapsed_time(self) -> None:
        key: str = f"dbinfo:{self.index.name.lower()}"
        base_value: dict = {"last_updated": int(time.time()-self.update_interval-100)}
        await connection.hmset(key, mapping=base_value)

    async def get_index_info(self):
        d = await connection.ft(self.index.name.lower()).info()
        return d.get("num_docs")

    async def update_db(self) -> None:
        can_be_updated: bool = all(
            [
                await self.index.index_exists(),
                await self.set_time_has_lapsed(),
            ]
        )

        if can_be_updated:
            await self.download_file()
            commands: int = 0

            with open(self.file_path, mode="r", encoding="utf-8") as csvfile:
                rdr = csv.DictReader(csvfile)

                for row in rdr:
                    row = self.model(**row)

                    await self.pipeline.hmset(
                        self.redis_key(row),
                        mapping=row.dict(),
                    )
                    commands += 1

                    if commands >= self.max_allowed_commands:
                        self.pipeline = await self.update_db_info(pipe=self.pipeline)
                        await self.pipeline.execute()
                        commands = 0

            if len(self.pipeline) > 0:
                self.pipeline = await self.update_db_info(pipe=self.pipeline)
                await self.pipeline.execute()
            return f"Database updated - {self.file_name}"
        else:
            raise WithinSetTime

    async def download_file(self) -> None:
        self.file_name: str = os.path.basename(self.url)
        self.file_path: str = os.path.realpath(self.base_dir + self.file_name)

        async with aiohttp.ClientSession() as session:
            async with aiofiles.open(self.file_path, mode="wb") as f:
                async with session.get(self.url) as resp:
                    async for chunk in resp.content.iter_chunked(1024 * 1024):
                        await f.write(chunk)
                return f"Downloaded - {self.file_name}"


class ManageCountries(RedisDBBase):
    """
    Adds countries to redis db
    TODO File download and database update should be automated with one command
    Make sure redisearch index exists before adding data
    """

    url: str = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/countries.csv"
    index = CountryIndex()
    model = Country

    def redis_key(self, row):
        return f"{self.index.prefix}{row.id}"


class ManageStates(RedisDBBase):
    """
    At the moment, states information is not being used for any API
    So, no need to index states data, however, code is implemented, just in case
    """

    url: str = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/states.csv"
    index = StateIndex()
    model = State

    def redis_key(self, row):
        return f"{self.index.prefix}{row.id}:country:{row.country_id}"


class ManageCities(RedisDBBase):
    url: str = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/cities.csv"
    index = CityIndex()
    model = City

    def redis_key(self, row):
        return (
            f"{self.index.prefix}{row.id}:state:{row.state_id}:country:{row.country_id}"
        )


class ManageTimezones(RedisDBBase):
    """
    Timezones is included as an array along with country
    There are many countries with more than one timezone
    Redis does not support nested hashes and redis indexes need to be flat
    So, we have to build separate index for timezones
    """

    url: str = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/countries.csv"
    index = TimeZoneIndex()
    model = TimeZone

    def redis_key(self, row):
        return f"{self.index.prefix}{row.id}:country:{row.country_id}"

    async def update_db(self) -> None:
        re_ptrn: re.Pattern = re.compile(
            r"zoneName:(?P<zone_name>[^(,)]+),gmtOffset:(?P<gmt_offset>[^(,)]+),gmtOffsetName:(?P<gmt_offset_name>[^(,)]+),abbreviation:(?P<abbreviation>[^(,)]+),tzName:(?P<tz_name>[^(})]+)"
        )

        can_be_updated: bool = all(
            [
                await self.index.index_exists(),
                await self.set_time_has_lapsed(),
            ]
        )

        if can_be_updated:
            await self.download_file()
            commands: int = 0

            with open(self.file_path, mode="r", encoding="utf-8") as csvfile:
                rdr: csv.DictReader = csv.DictReader(csvfile)
                id_counter: int = 0

                for row in rdr:
                    all_zones: list = re.findall(r"\{.+?\}", row.get("timezones"))

                    for zone in all_zones:
                        m = re_ptrn.search(zone)
                        id_counter += 1
                        tz = self.model()
                        tz.id = id_counter
                        tz.zone_name = (
                            m.group("zone_name").replace("\\", "").replace("'", "")
                        )
                        tz.gmt_offset = m.group("gmt_offset").replace("'", "")
                        tz.gmt_offset_name = m.group("gmt_offset_name").replace("'", "")
                        tz.abbreviation = m.group("abbreviation").replace("'", "")
                        tz.tz_name = m.group("tz_name").replace("'", "")
                        tz.country_id = row.get("id")
                        tz.country_name = row.get("name")
                        tz.emoji = row.get("emoji")

                        await self.pipeline.hmset(
                            self.redis_key(tz),
                            mapping=tz.dict(),
                        )
                        commands += 1

                    self.pipeline = await self.update_db_info(pipe=self.pipeline)
                    await self.pipeline.execute()
                    commands = 0

            if len(self.pipeline) > 0:
                self.pipeline = await self.update_db_info(pipe=self.pipeline)
                await self.pipeline.execute()
        else:
            raise WithinSetTime


def humanized_delta(timestamp: int) -> str:
    now: datetime = datetime.datetime.now()
    then: datetime = datetime.datetime.fromtimestamp(timestamp)
    delta: datetime = now - then
    return humanize.naturaldelta(delta)


async def build_db_info() -> dict:

    r: dict = await connection.info()
    indexes: list = await connection.execute_command("FT._LIST")
    index_info: list = []

    for index in indexes:
        i: dict = await connection.ft(index).info() if r else {}

        last_db_update_epoch: list = (
            await connection.hmget(f"dbinfo:{index}", "last_updated") if r else ["0"]
        )
        index_info.append(
            {
                "index_name": index,
                "number_of_records": i.get("num_docs", ""),
                "last_updated": f"{humanized_delta(int(last_db_update_epoch[0]))}",
            }
        )

    result = {
        "uptime_in_seconds": r.get("uptime_in_seconds", ""),
        "uptime_in_days": r.get("uptime_in_days", ""),
        "memory_in_use": r.get("used_memory_human", ""),
        "total_keys": r.get("db0", {}).get("keys", 0),
        "total_indexes": len(indexes) if indexes else 0,
        "index_info": index_info,
    }

    return result
