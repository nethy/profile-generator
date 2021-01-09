from dataclasses import dataclass
from typing import Any, List

from .schema import Schema, SchemaError
from .type_schema import InvalidTypeError


class OptionsSchema(Schema):
    def __init__(self, *options: str):
        self._options = [option.casefold() for option in options]
        self._error = InvalidOptionError(list(options))

    def validate(self, data: Any) -> List[SchemaError]:
        if not isinstance(data, str):
            return [InvalidTypeError(str)]

        if data.casefold() not in self._options:
            return [self._error]
        else:
            return []


@dataclass
class InvalidOptionError(SchemaError):
    expected_options: List[str]


def options_of(*options: str) -> OptionsSchema:
    return OptionsSchema(*options)
