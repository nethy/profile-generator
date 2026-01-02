from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Any, NamedTuple, Optional


class SchemaError(Exception, metaclass=ABCMeta):
    pass


class Schema(metaclass=ABCMeta):
    @abstractmethod
    def validate(self, data: Any) -> Optional[SchemaError]:
        pass


class SchemaField(NamedTuple):
    name: str
    default_value: Any
