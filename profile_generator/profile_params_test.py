from enum import unique
from typing import Final
from unittest import TestCase

from profile_generator.profile_params import ProfileParamEnum, ProfileParamParser, Value


class DummyParams(ProfileParamParser):
    def __init__(self, param: int):
        self.param: Final = Value[int](param)


@unique
class DummyEnum(ProfileParamEnum):
    APPLE = "Apple"
    BANANE = "Banana"


class ProfileParamsTest(TestCase):
    def test_text_enum_parse(self) -> None:
        self.assertEqual(DummyEnum.parse("apple"), DummyEnum.APPLE)
        self.assertIsNone(DummyEnum.parse("cucumber"))
