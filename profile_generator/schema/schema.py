from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Any, Optional


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
