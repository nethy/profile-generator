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
                Point(x=0.098039, y=0.019012),
                Point(x=0.211765, y=0.126845),
                Point(x=0.286275, y=0.299108),
                Point(x=0.380392, y=0.577756),
                Point(x=0.529412, y=0.828917),
                Point(x=0.737255, y=0.946303),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_calculate_brightness(self) -> None:
        self.assertEqual(
            calculate(_GREY18, _SLOPE, _BRIGHTNESS),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.129412, y=0.116303),
                Point(x=0.180392, y=0.272618),
                Point(x=0.235294, y=0.488977),
                Point(x=0.262745, y=0.583431),
                Point(x=0.313725, y=0.712499),
                Point(x=0.396078, y=0.831673),
                Point(x=0.537255, y=0.918683),
                Point(x=0.662745, y=0.953855),
                Point(x=1.000000, y=1.000000),
            ],
        )
