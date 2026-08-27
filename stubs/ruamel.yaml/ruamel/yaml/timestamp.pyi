from datetime import datetime, timedelta, tzinfo
from typing import Literal
from typing_extensions import Self

class TimeStamp(datetime):
    _yaml: dict[str, bool | str | timedelta | int | None]
    # copilot: timestamp.py mirrors datetime construction, then initializes YAML formatting state in __init__.
    def __new__(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: tzinfo | None = None,
        *,
        fold: int = 0,
    ) -> Self: ...
    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tzinfo: tzinfo | None = None,
        *,
        fold: int = 0,
    ) -> None: ...
    def __deepcopy__(self, memo: object) -> TimeStamp: ...
    # copilot: timestamp.py uses None as a preserve-current sentinel and True to preserve tzinfo in replace().
    def replace(
        self,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        hour: int | None = None,
        minute: int | None = None,
        second: int | None = None,
        microsecond: int | None = None,
        tzinfo: tzinfo | Literal[True] | None = True,
        fold: int | None = None,
    ) -> Self: ...
    def __str__(self) -> str: ...
