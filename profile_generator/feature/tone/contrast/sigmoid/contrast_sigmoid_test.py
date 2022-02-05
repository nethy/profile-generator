from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY18 = 87.0
_SLOPE = 2.5


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.103175, y=0.028210),
                Point(x=0.206349, y=0.134297),
                Point(x=0.269841, y=0.273313),
                Point(x=0.380952, y=0.568239),
                Point(x=0.531746, y=0.811383),
                Point(x=0.634921, y=0.891116),
                Point(x=0.753968, y=0.944555),
                Point(x=1.000000, y=1.000000),
            ],
        )
