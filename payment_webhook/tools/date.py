import datetime
from typing import Optional

import pytz


def str_to_datetime(
    raw_date: str | datetime.datetime,
    accepted_date_formats: Optional[list[str] | None] = None,
    ignore_tzinfo: Optional[bool] = None,
) -> datetime.datetime:
    """Convert a date string to a datetime object based on ISO and some extra accepted
    formats. If the input already is a datetime, it is returned.
    """
    accepted_input_datetime_formats = [
        "%Y-%m-%dT%H:%M:%S+00:00",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
    ]
    if isinstance(raw_date, datetime.datetime):
        return raw_date
    try:
        return datetime.datetime.fromisoformat(raw_date).replace(tzinfo=pytz.utc)
    except ValueError as error:
        if accepted_date_formats is None:
            accepted_date_formats = accepted_input_datetime_formats
        if ignore_tzinfo is None:
            ignore_tzinfo = True
        for date_format in accepted_date_formats:
            try:
                date = datetime.datetime.strptime(raw_date, date_format)
                if ignore_tzinfo:
                    return date.replace(tzinfo=pytz.utc)
                return date
            except ValueError:
                continue
        raise ValueError(f"{raw_date} is not a ISO or acceptable datetime.") from error


def birth_date_to_age(
    birth: str | datetime.datetime,
    accepted_date_formats: Optional[list[str] | None] = None,
    ignore_tzinfo: Optional[bool] = None,
) -> int:
    """
    Calculates the age of a person based on a birth date.
    """
    if isinstance(birth, str):
        birth = str_to_datetime(birth, accepted_date_formats, ignore_tzinfo)
    today = datetime.date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def to_br_date_str(
    iso_datetime: str | datetime.datetime,
    accepted_date_formats: Optional[list[str] | None] = None,
    ignore_tzinfo: Optional[bool] = None,
) -> str:
    """Converts a YYYY-mm-dd date string to '%Y-%m-%dT%H:%M:%S.%fZ'"""
    if isinstance(iso_datetime, str):
        iso_datetime = str_to_datetime(iso_datetime, accepted_date_formats, ignore_tzinfo)
    return iso_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def to_datetime_str(
    iso_datetime: str | datetime.datetime,
    accepted_date_formats: Optional[list[str] | None] = None,
    ignore_tzinfo: Optional[bool] = None,
) -> str:
    """Converts a YYYY-mm-dd date string to '%Y-%m-%dT%H:%M:%S.%fZ'."""
    if isinstance(iso_datetime, str):
        iso_datetime = str_to_datetime(iso_datetime, accepted_date_formats, ignore_tzinfo)
    return iso_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
