import datetime
import json
import re
from typing import Any, Callable, Dict

from bson import ObjectId

from . import date

WHITESPACE = re.compile(r"[ \t\n\r]*", re.VERBOSE | re.MULTILINE | re.DOTALL)


class Encoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return date.to_datetime_str(o)
        return json.JSONEncoder.default(self, o)


class Decoder(json.JSONDecoder):
    def decode(self, s: str, _w: Callable = WHITESPACE.match) -> Dict:
        json_obj = super().decode(s)
        return self._re_decode(json_obj)

    def _re_decode(self, json_obj: Any) -> Any:
        if isinstance(json_obj, str):
            try:
                return date.str_to_datetime(json_obj)
            except ValueError:
                return json_obj
        if isinstance(json_obj, list):
            return [self._re_decode(value) for value in json_obj]
        if isinstance(json_obj, dict):
            return {key: self._re_decode(value) for key, value in json_obj.items()}
        return json_obj
