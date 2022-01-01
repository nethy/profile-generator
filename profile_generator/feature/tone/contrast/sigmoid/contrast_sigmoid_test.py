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
                Point(x=0.095238, y=0.021819),
                Point(x=0.206349, y=0.127925),
                Point(x=0.253968, y=0.231352),
                Point(x=0.309524, y=0.382838),
                Point(x=0.373016, y=0.544080),
                Point(x=0.452381, y=0.706356),
                Point(x=0.539683, y=0.822759),
                Point(x=0.761905, y=0.951902),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.023492),
                Point(x=0.142857, y=0.114557),
                Point(x=0.182540, y=0.230199),
                Point(x=0.230159, y=0.410370),
                Point(x=0.285714, y=0.598307),
                Point(x=0.349206, y=0.756455),
                Point(x=0.420635, y=0.854534),
                Point(x=0.539683, y=0.928557),
                Point(x=0.674603, y=0.965301),
                Point(x=1.000000, y=1.000000),
            ],
        )
