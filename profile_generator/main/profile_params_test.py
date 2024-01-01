from enum import unique
from typing import Final
from unittest import TestCase

from profile_generator.main import ProfileParamEnum, ProfileParamParser, Value


@unique
class DummyEnum(ProfileParamEnum):
    APPLE = "Apple"
    BANANA = "Banana"


class NestedParams(ProfileParamParser):
    def __init__(self) -> None:
        self.param: Final = Value[int](1)


class DummyParams(ProfileParamParser):
    def __init__(self) -> None:
        self.int_param: Final = Value[int](2)
        self.enum_param: Final = Value[DummyEnum](DummyEnum.APPLE)
        self.nested_param: Final = NestedParams()


class ProfileParamsTest(TestCase):
    def setUp(self) -> None:
        self.dummy_params = DummyParams()

    def test_parse_default(self) -> None:
        self.dummy_params.parse({})
        self._assert_params(2, DummyEnum.APPLE, 1)

    def test_parse(self) -> None:
        data = {"int_param": 3, "enum_param": "BANANA", "nested_param": {"param": 4}}
        self.dummy_params.parse(data)
        self._assert_params(3, DummyEnum.BANANA, 4)

    def _assert_params(
        self,
        int_param: int,
        enum_param: DummyEnum,
        nested_param: int,
    ) -> None:
        self.assertEqual(self.dummy_params.int_param.value, int_param)
        self.assertEqual(self.dummy_params.enum_param.value, enum_param)
        self.assertEqual(self.dummy_params.nested_param.param.value, nested_param)
