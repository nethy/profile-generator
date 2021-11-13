from unittest import TestCase

from .contrast_sigmoid import Point, calculate

_GREY18 = 87.0
_SLOPE = 2.5
_BRIGHTNESS = 1.0


class ContrastSigmoid(TestCase):
    def test_calculate(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.103175, y=0.017096),
                Point(x=0.206349, y=0.113215),
                Point(x=0.253968, y=0.215814),
                Point(x=0.325397, y=0.421849),
                Point(x=0.373016, y=0.546336),
                Point(x=0.444444, y=0.686918),
                Point(x=0.547619, y=0.821750),
                Point(x=0.761905, y=0.954804),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.018024),
                Point(x=0.134921, y=0.099848),
                Point(x=0.182540, y=0.248891),
                Point(x=0.230159, y=0.443471),
                Point(x=0.261905, y=0.553050),
                Point(x=0.396825, y=0.802005),
                Point(x=0.515873, y=0.890142),
                Point(x=0.658730, y=0.947648),
                Point(x=1.000000, y=1.000000),
            ],
        )
