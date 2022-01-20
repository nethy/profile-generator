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
                Point(x=0.103175, y=0.026549),
                Point(x=0.206349, y=0.132109),
                Point(x=0.388889, y=0.588293),
                Point(x=0.539683, y=0.828450),
                Point(x=0.642857, y=0.904344),
                Point(x=0.761905, y=0.953098),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.071429, y=0.024666),
                Point(x=0.142857, y=0.118778),
                Point(x=0.285714, y=0.606533),
                Point(x=0.349206, y=0.764514),
                Point(x=0.412698, y=0.851318),
                Point(x=0.531746, y=0.927240),
                Point(x=0.674603, y=0.966199),
                Point(x=1.000000, y=1.000000),
            ],
        )
