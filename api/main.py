from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime
import pytz
import re
from typing import Dict, Tuple

app = FastAPI(
    title="Automate All The Things API",
    description="""
An API that returns the current UTC time and a static message 'Automate All The Things'.

Endpoints:
- `/`: Returns the message and current UTC time in ISO8601.
- `/format_time/{format_code}`: Returns the time in various formats and optional timezones.
- `/formats`: Lists all available format codes.
- `/healthz`: Health check.

For a list of supported time formats, call `/formats`.

Timezones should be valid IANA timezone strings (e.g., 'America/New_York').
""",
    version="1.0.0",
    contact={
        "name": "Dilhan Akyuz",
        "email": "dilhan.akyuz72@gmail.com",
    }
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "detail": (
                    "The requested endpoint does not exist. "
                    "Please refer to the API documentation at `/docs` or `/formats` for available endpoints and formats."
                )
            }
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

FormatConfig = Dict[str, Tuple[str, bool]]

TIME_FORMATS: FormatConfig = {
    "iso8601": ("%Y-%m-%dT%H:%M:%S%z", False),
    "log_millis": ("%Y-%m-%d %H:%M:%S,%f", True),
    "euro_tz": ("%d/%b/%Y:%H:%M:%S %z", False),
    "us_ampm": ("%b %d, %Y %I:%M:%S %p", False),
    "with_millis_tzname": ("%Y %b %d %H:%M:%S.%f %Z", True),
}

def get_current_utc() -> datetime:
    """Get current datetime in UTC."""
    return datetime.now(pytz.UTC)

def format_time_str(dt: datetime, fmt: str, truncate_millis: bool) -> str:
    """
    Format the given datetime with the provided strftime pattern.
    If truncate_millis is True, we truncate microseconds to milliseconds.
    """
    formatted = dt.strftime(fmt)
    if truncate_millis:
        match = re.search(r'(\d{6})', formatted)
        if match:
            full_micro = match.group(1)
            millis = full_micro[:3]
            formatted = formatted[:match.start()] + millis + formatted[match.end():]
    return formatted

@app.get("/", tags=["Core"], summary="Get the current UTC time and the static message")
def read_root():
    """
    Returns:
    - The static message "Automate All The Things"
    - The current UTC time in ISO8601 format (default standard)
    """
    dt = get_current_utc()
    default_format, truncate_millis = TIME_FORMATS["iso8601"]
    current_time = format_time_str(dt, default_format, truncate_millis)
    return {
        "message": "Automate All The Things",
        "current_time": current_time
    }

@app.get("/format_time/{format_code}", tags=["Core"], summary="Get the current time in a specified format and timezone")
def format_time(format_code: str, tz: str = Query("UTC", description="Specify a valid IANA timezone (e.g. 'America/New_York'). Defaults to 'UTC'.")):
    """
    Returns the current time in one of the predefined formats, optionally converted to a given timezone.
    
    **Available format_code values:**
    - `iso8601` : yyyy-MM-dd'T'HH:mm:ssZZZZ
    - `log_millis` : yyyy-MM-dd HH:mm:ss,SSS
    - `euro_tz` : dd/MMM/yyyy:HH:mm:ss ZZZZ
    - `us_ampm` : MMM dd, yyyy hh:mm:ss a
    - `with_millis_tzname` : yyyy MMM dd HH:mm:ss.SSS zzz

    For a list of all available formats, use GET /formats.
    Example usage:
    - GET /format_time/iso8601
    - GET /format_time/iso8601?tz=America/New_York
    """
    if format_code not in TIME_FORMATS:
        raise HTTPException(
            status_code=400, 
            detail=(
                f"Invalid format_code '{format_code}'. "
                f"Available formats: {list(TIME_FORMATS.keys())}. "
                "Please consult /formats for details."
            )
        )
    
    try:
        user_tz = pytz.timezone(tz)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(
            status_code=400, 
            detail=(
                f"Unknown timezone '{tz}' specified. "
                "Please provide a valid IANA timezone. "
                "Examples: 'UTC', 'America/New_York', 'Europe/London'. "
                "Refer to https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for a full list."
            )
        )

    dt_utc = get_current_utc()
    dt_local = dt_utc.astimezone(user_tz)
    fmt, truncate_millis = TIME_FORMATS[format_code]
    formatted_time = format_time_str(dt_local, fmt, truncate_millis)

    return {
        "format_code": format_code,
        "timezone": tz,
        "formatted_time": formatted_time
    }

@app.get("/formats", tags=["Core"], summary="List all available formats")
def list_formats():
    """
    Returns a list of all available format codes along with an example using the current UTC time.
    Use these codes with /format_time/{format_code}.
    """
    dt = get_current_utc()
    examples = {}
    for code, (fmt, truncate_millis) in TIME_FORMATS.items():
        sample_output = format_time_str(dt, fmt, truncate_millis)
        examples[code] = sample_output
    return {"available_formats": examples}

@app.get("/healthz", tags=["Health"], summary="Health check endpoint")
def health_check():
    """
    Health check endpoint to verify that the service is running.
    Returns a simple JSON object confirming 'status: ok'.
    """
    return {"status": "ok"}
