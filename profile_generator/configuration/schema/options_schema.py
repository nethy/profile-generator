from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError


class OptionsSchema(Schema):
    def __init__(self, *options: str):
        self._options = [option.casefold() for option in options]
        self._error = InvalidOptionError(options)

    def validate(self, data: Any) -> list[SchemaError]:
        if not isinstance(data, str):
            return [InvalidTypeError(str)]

        if data.casefold() not in self._options:
            return [self._error]
        else:
            return []


@dataclass
class InvalidOptionError(SchemaError):
    expected_options: Sequence[str]


def options_of(*options: str) -> OptionsSchema:
    return OptionsSchema(*options)
