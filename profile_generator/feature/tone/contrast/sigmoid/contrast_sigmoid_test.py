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
                Point(x=0.095238, y=0.019425),
                Point(x=0.206349, y=0.127011),
                Point(x=0.293651, y=0.335943),
                Point(x=0.388889, y=0.589907),
                Point(x=0.460317, y=0.736328),
                Point(x=0.539683, y=0.840271),
                Point(x=0.642857, y=0.915444),
                Point(x=0.761905, y=0.960424),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.021025),
                Point(x=0.142857, y=0.113354),
                Point(x=0.214286, y=0.346816),
                Point(x=0.285714, y=0.608748),
                Point(x=0.349206, y=0.774140),
                Point(x=0.412698, y=0.863418),
                Point(x=0.531746, y=0.936976),
                Point(x=0.674603, y=0.971899),
                Point(x=1.000000, y=1.000000),
            ],
        )
