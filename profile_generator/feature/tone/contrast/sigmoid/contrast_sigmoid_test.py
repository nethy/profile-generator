from unittest import TestCase

from .contrast_sigmoid import Point, contrast, flat

_GREY18 = 87 / 255
_SLOPE = 2.5


class ContrastSigmoid(TestCase):
    def test_flat(self) -> None:
        self.assertEqual(
            flat(_GREY18),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.013289, y=0.028541),
                Point(x=0.023256, y=0.049228),
                Point(x=0.033223, y=0.065936),
                Point(x=0.049834, y=0.089179),
                Point(x=0.076412, y=0.125611),
                Point(x=0.142857, y=0.215566),
                Point(x=0.285714, y=0.397249),
                Point(x=0.428571, y=0.553810),
                Point(x=0.571429, y=0.683765),
                Point(x=0.714286, y=0.794806),
                Point(x=0.857143, y=0.897465),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_contrast(self) -> None:
        self.assertEqual(
            contrast(_GREY18, _SLOPE),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.049834, y=0.005966),
                Point(x=0.142857, y=0.027387),
                Point(x=0.285714, y=0.125254),
                Point(x=0.355482, y=0.231083),
                Point(x=0.428571, y=0.385238),
                Point(x=0.514950, y=0.584784),
                Point(x=0.571429, y=0.699326),
                Point(x=0.641196, y=0.806714),
                Point(x=0.714286, y=0.882344),
                Point(x=0.857143, y=0.962650),
                Point(x=0.943522, y=0.988238),
                Point(x=1.000000, y=1.000000),
            ],
        )
