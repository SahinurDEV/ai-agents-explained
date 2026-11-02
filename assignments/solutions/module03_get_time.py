"""Module 3 solution: a get_time tool. Paste into project/common/tools.py."""
from datetime import datetime
from zoneinfo import ZoneInfo

CITY_TZ = {"dhaka": "Asia/Dhaka", "tokyo": "Asia/Tokyo", "london": "Europe/London", "new york": "America/New_York"}


def get_time(city: str) -> str:
    tz = CITY_TZ.get(city.lower())
    if not tz:
        return f"error: unknown city {city!r}; known: {', '.join(CITY_TZ)}"
    return f"Local time in {city}: {datetime.now(ZoneInfo(tz)).strftime('%H:%M, %A')}"

# Schema:  schema("get_time", "Get the current local time for a city.", city=("string", "City name"))

if __name__ == "__main__":
    print(get_time("Dhaka")); print(get_time("Atlantis"))
