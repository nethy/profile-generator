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
                Point(x=0.087302, y=0.008290),
                Point(x=0.198413, y=0.097397),
                Point(x=0.277778, y=0.291094),
                Point(x=0.380952, y=0.570444),
                Point(x=0.452381, y=0.722738),
                Point(x=0.539683, y=0.840271),
                Point(x=0.650794, y=0.919469),
                Point(x=0.761905, y=0.960424),
                Point(x=1.000000, y=1.000000),
            ],
        )
