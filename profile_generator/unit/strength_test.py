import unittest

from .strength import Strength


class StrengthTest(unittest.TestCase):
    def test_invalid_strength(self) -> None:
        self.assertRaises(ValueError, Strength, -1.1)
        self.assertRaises(ValueError, Strength, 1.1)

    def test_repr(self) -> None:
        self.assertEqual("Strength(value=0.500000)", Strength(0.5).__repr__())
