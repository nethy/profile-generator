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
                Point(x=0.011765, y=0.025163),
                Point(x=0.023529, y=0.049478),
                Point(x=0.039216, y=0.074164),
                Point(x=0.066667, y=0.111538),
                Point(x=0.105882, y=0.164512),
                Point(x=0.211765, y=0.303570),
                Point(x=0.482353, y=0.613440),
                Point(x=0.796078, y=0.875153),
                Point(x=0.921569, y=0.955380),
                Point(x=1.000000, y=1.000000),
            ],
        )

    def test_contrast(self) -> None:
        self.assertEqual(
            contrast(_GREY18, _SLOPE),
            [
                Point(x=0.000000, y=0.000000),
                Point(x=0.156863, y=0.033880),
                Point(x=0.301961, y=0.149322),
                Point(x=0.352941, y=0.229918),
                Point(x=0.411765, y=0.349194),
                Point(x=0.537255, y=0.629822),
                Point(x=0.607843, y=0.756344),
                Point(x=0.682353, y=0.849817),
                Point(x=0.819608, y=0.945690),
                Point(x=0.937255, y=0.986251),
                Point(x=1.000000, y=1.000000),
            ],
        )
