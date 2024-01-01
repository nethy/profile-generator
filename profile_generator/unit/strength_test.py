import unittest

from .strength import Strength


class StrengthTest(unittest.TestCase):
    def test_invalid_strength(self) -> None:
        self.assertRaises(ValueError, Strength, -1.1)
        self.assertRaises(ValueError, Strength, 1.1)
        self.assertRaises(ValueError, Strength.non_negative, -0.1)

    def test_repr(self) -> None:
        self.assertEqual("Strength(value=0.5000000)", repr(Strength(0.5)))
