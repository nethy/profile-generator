from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Any, NamedTuple, Optional

from profile_generator.profile_input import ProfileInput


class SchemaError(Exception, metaclass=ABCMeta):
    pass


class Schema(metaclass=ABCMeta):
    @abstractmethod
    def validate(self, data: Any) -> Optional[SchemaError]:
        pass

    def process(  # pylint: disable=no-self-use
        self, data: Any  # pylint: disable=unused-argument
    ) -> Mapping[str, str]:
        return {}

    def parse(  # pylint: disable=no-self-use
        self, data: Any, profile_input: ProfileInput  # pylint: disable=unused-argument
    ) -> None:
        pass


class SchemaField(NamedTuple):
    name: str
    default_value: Any
