from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY18 = 87.0
_SLOPE = 2.5


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE),
            (
                [
                    Point(x=0.000000, y=0.000000),
                    Point(x=0.055556, y=0.093075),
                    Point(x=0.150794, y=0.234257),
                    Point(x=0.412698, y=0.540821),
                    Point(x=0.777778, y=0.850873),
                    Point(x=1.000000, y=1.000000),
                ],
                [
                    Point(x=0.000000, y=0.000000),
                    Point(x=0.142857, y=0.023815),
                    Point(x=0.269841, y=0.098621),
                    Point(x=0.380952, y=0.271176),
                    Point(x=0.523810, y=0.596783),
                    Point(x=0.626984, y=0.770944),
                    Point(x=0.785714, y=0.914897),
                    Point(x=1.000000, y=1.000000),
                ],
            ),
        )
