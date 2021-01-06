import unittest
from typing import TypeVar
from unittest.mock import Mock

from .marshaller import get_profile_args

T = TypeVar("T")


class ResolverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.marshallers = {"stub": self.identity, "other_stub": self.identity}

    def test_marshal_returns_empty_when_no_resolvers_exist(self) -> None:
        self.assertEqual({}, get_profile_args({"a": 1}))

    @staticmethod
    def test_marshal_invokes_resolvers_with_empty_config_if_not_exist() -> None:
        config = {"no_stub": {"a": 1}}
        marshaller = Mock(return_value={})

        get_profile_args(config, stub=marshaller)

        marshaller.assert_called_with({})

    def test_marshal_ivokes_resolver_with_matching_config(self) -> None:
        config = dict(stub={"a": 1}, other_stub={"b": 2})

        self.assertEqual({"a": 1, "b": 2}, get_profile_args(config, **self.marshallers))

    def test_marshal_overwrites_configs_returned_by_resolvers(self) -> None:
        config = {"stub": {"a": 1}, "other_stub": {"a": 2}}

        self.assertEqual({"a": 2}, get_profile_args(config, **self.marshallers))

    def test_marhsal_invokes_resolver_by_hierarchical_key(self) -> None:
        config = {"nested": {"member": {"a": 1}}}
        marshaller = {"nested.member": self.identity}

        self.assertEqual({"a": 1}, get_profile_args(config, **marshaller))

    @staticmethod
    def identity(x: T) -> T:
        return x
