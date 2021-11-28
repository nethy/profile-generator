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
                Point(x=0.198413, y=0.134549),
                Point(x=0.269841, y=0.283769),
                Point(x=0.373016, y=0.541330),
                Point(x=0.531746, y=0.785196),
                Point(x=0.753968, y=0.929483),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.142857, y=0.134532),
                Point(x=0.182540, y=0.244725),
                Point(x=0.246032, y=0.467627),
                Point(x=0.277778, y=0.568575),
                Point(x=0.412698, y=0.817105),
                Point(x=0.539683, y=0.904882),
                Point(x=0.674603, y=0.950637),
                Point(x=1.000000, y=1.000000),
            ],
        )
