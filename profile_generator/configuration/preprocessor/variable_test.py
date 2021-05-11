from typing import Any, MutableMapping
from unittest import TestCase

from .variable import (
    IllegalReferenceError,
    UndefinedVariableError,
    VariableError,
    replace,
)


class VariableTest(TestCase):
    def test_replace_empty(self) -> None:
        self.assertEqual(({}, []), replace({}))

    def test_replace_no_variables(self) -> None:
        data = {"a": 1}

        self.assertEqual((data, []), replace(data))

    def test_replace_remove_variables_item(self) -> None:
        data = {"variables": {"var": 2}, "a": 1}

        self.assertEqual(({"a": 1}, []), replace(data))

    def test_replace_variables(self) -> None:
        data = {"variables": {"a": 1}, "a": "$a"}

        self.assertEqual(({"a": 1}, []), replace(data))

    def test_replace_variables_in_dict(self) -> None:
        data = {"variables": {"b": 1}, "a": {"b": "$b"}}

        self.assertEqual(({"a": {"b": 1}}, []), replace(data))

    def test_replace_variables_in_list(self) -> None:
        data = {"variables": {"x": 1, "y": 2}, "a": ["$x", "$y"]}

        self.assertEqual(({"a": [1, 2]}, []), replace(data))

    def test_replace_undefined_variable_error(self) -> None:
        self._assert_error(UndefinedVariableError("a.$a"), {"a": "$a"})
        self._assert_error(UndefinedVariableError("a[0].$a"), {"a": ["$a"]})
        self._assert_error(UndefinedVariableError("a.b.$a"), {"a": {"b": "$a"}})

    def test_replace_invalid_variable_error(self) -> None:
        self._assert_error(IllegalReferenceError("$a"), {"$a": 1})
        self._assert_error(IllegalReferenceError("a.$b"), {"a": {"$b": 1}})

    def _assert_error(
        self, error: VariableError, data: MutableMapping[str, Any]
    ) -> None:
        self.assertEqual(({}, [error]), replace(data))
