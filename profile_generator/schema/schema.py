from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class SchemaError(Exception, metaclass=ABCMeta):
    ...


class Schema(metaclass=ABCMeta):
    @abstractmethod
    def validate(self, data: Any) -> Optional[SchemaError]:
        ...
