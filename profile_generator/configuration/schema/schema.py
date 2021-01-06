from abc import ABCMeta, abstractmethod
from typing import Any, List


class SchemaError(Exception, metaclass=ABCMeta):
    pass


class Schema(metaclass=ABCMeta):
    """
    mypy doesn't like Optional or Union types at this moment,
    therefore using List as a workaround.
    """

    @abstractmethod
    def validate(self, data: Any) -> List[SchemaError]:
        pass
