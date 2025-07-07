from unittest import TestCase

from .contrast_sigmoid import Point, get_contrast, get_flat

_GREY18 = 0.08
_SLOPE = 2.5


class ContrastSigmoid(TestCase):
    def test_get_flat(self) -> None:
        self.assertEqual(
            get_flat(_GREY18),
            [
                Point(x=0.0000000, y=0.0000000),
                Point(x=0.0235294, y=0.0602800),
                Point(x=0.0666667, y=0.1284990),
                Point(x=0.4000000, y=0.5614754),
                Point(x=1.0000000, y=1.0000000),
            ],
        )

    def test_get_contrast(self) -> None:
        self.assertEqual(
            get_contrast(_SLOPE),
            [
                Point(x=0.0000000, y=0.0000000),
                Point(x=0.1882353, y=0.0100357),
                Point(x=0.2470588, y=0.0447551),
                Point(x=0.3215686, y=0.1439049),
                Point(x=0.4274510, y=0.3693628),
                Point(x=0.5333333, y=0.6288578),
                Point(x=0.6313725, y=0.8144289),
                Point(x=0.7764706, y=0.9494787),
                Point(x=0.8549020, y=0.9786944),
                Point(x=1.0000000, y=1.0000000),
            ],
        )
