from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Mapping
from typing import Any, Optional, TypeVar

T = TypeVar("T")
PROCESSOR = Callable[[T], Mapping[str, str]]


class SchemaError(Exception, metaclass=ABCMeta):
    ...


class Schema(metaclass=ABCMeta):
    @abstractmethod
    def validate(self, data: Any) -> Optional[SchemaError]:
        ...

    def process(  # pylint: disable=no-self-use
        self, data: Any  # pylint: disable=unused-argument
    ) -> Mapping[str, str]:
        return {}
