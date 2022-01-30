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
                Point(x=0.087302, y=0.016503),
                Point(x=0.206349, y=0.127011),
                Point(x=0.293651, y=0.335943),
                Point(x=0.380952, y=0.571407),
                Point(x=0.460317, y=0.746076),
                Point(x=0.539683, y=0.856164),
                Point(x=0.642857, y=0.930287),
                Point(x=0.746032, y=0.966116),
                Point(x=1.000000, y=1.000000),
            ],
        )
