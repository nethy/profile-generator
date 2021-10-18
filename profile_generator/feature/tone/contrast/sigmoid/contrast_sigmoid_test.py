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
                Point(x=0.111111, y=0.016092),
                Point(x=0.214286, y=0.106447),
                Point(x=0.269841, y=0.236573),
                Point(x=0.325397, y=0.416216),
                Point(x=0.373016, y=0.556571),
                Point(x=0.452381, y=0.720436),
                Point(x=0.547619, y=0.846684),
                Point(x=0.682540, y=0.939380),
                Point(x=0.801587, y=0.975547),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.014108),
                Point(x=0.142857, y=0.096512),
                Point(x=0.182540, y=0.221201),
                Point(x=0.230159, y=0.433482),
                Point(x=0.269841, y=0.584670),
                Point(x=0.325397, y=0.724817),
                Point(x=0.412698, y=0.850802),
                Point(x=0.539683, y=0.934450),
                Point(x=0.674603, y=0.971500),
                Point(x=1.000000, y=1.000000),
            ],
        )
