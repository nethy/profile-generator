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
                Point(x=0.129412, y=0.018440),
                Point(x=0.258824, y=0.089654),
                Point(x=0.313725, y=0.158305),
                Point(x=0.368627, y=0.256570),
                Point(x=0.447059, y=0.428567),
                Point(x=0.513725, y=0.576181),
                Point(x=0.623529, y=0.757449),
                Point(x=0.780392, y=0.903141),
                Point(x=0.921569, y=0.973783),
                Point(x=1.000000, y=1.000000),
            ],
        )
