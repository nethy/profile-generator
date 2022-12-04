from typing import Any
from unittest import TestCase

from profile_generator.profile_params import NoneSafe

_DEFAULT_VALUE = "default_value"


class DummyNoneSafe(NoneSafe):
    field: Any = _DEFAULT_VALUE


class ProfileParamsTest(TestCase):
    def test_not_none_assignment(self) -> None:
        new_value = "new_value"
        dummy = DummyNoneSafe()
        dummy.field = new_value

        self.assertEqual(dummy.field, new_value)

    def test_none_assignment(self) -> None:
        dummy = DummyNoneSafe()
        dummy.field = None

        self.assertEqual(dummy.field, _DEFAULT_VALUE)
