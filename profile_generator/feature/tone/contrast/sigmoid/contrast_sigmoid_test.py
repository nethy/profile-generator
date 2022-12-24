from unittest import TestCase

from .contrast_sigmoid import Point, get_contrast, get_flat

_GREY18 = 87 / 255
_SLOPE = 2.5


class ContrastSigmoid(TestCase):
    def test_get_flat(self) -> None:
        self.assertEqual(
            get_flat(_GREY18),
            [
                Point(x=0.0000000, y=0.0000000),
                Point(x=0.0235294, y=0.0495445),
                Point(x=0.0549020, y=0.0957556),
                Point(x=0.0862745, y=0.1386135),
                Point(x=0.1176471, y=0.1813314),
                Point(x=0.1490196, y=0.2237998),
                Point(x=0.1803922, y=0.2658342),
                Point(x=0.2117647, y=0.3072038),
                Point(x=0.2431373, y=0.3476739),
                Point(x=0.2745098, y=0.3870376),
                Point(x=0.3098039, y=0.4297974),
                Point(x=0.3450980, y=0.4707909),
                Point(x=0.3803922, y=0.5099320),
                Point(x=0.4156863, y=0.5472006),
                Point(x=0.4509804, y=0.5826347),
                Point(x=0.4901961, y=0.6199598),
                Point(x=0.5294118, y=0.6552989),
                Point(x=0.5686275, y=0.6888653),
                Point(x=0.6078431, y=0.7208971),
                Point(x=0.6509804, y=0.7546545),
                Point(x=0.6941176, y=0.7871734),
                Point(x=0.7372549, y=0.8187437),
                Point(x=0.7803922, y=0.8496089),
                Point(x=0.8235294, y=0.8799533),
                Point(x=0.8666667, y=0.9098941),
                Point(x=0.9098039, y=0.9394783),
                Point(x=0.9529412, y=0.9686824),
                Point(x=0.9960784, y=0.9974160),
                Point(x=1.0000000, y=1.0000000),
            ],
        )

    def test_get_contrast(self) -> None:
        self.assertEqual(
            get_contrast(_GREY18, _SLOPE),
            [
                Point(x=0.0000000, y=0.0000000),
                Point(x=0.0509804, y=0.0114703),
                Point(x=0.0980392, y=0.0344607),
                Point(x=0.1372549, y=0.0657148),
                Point(x=0.1764706, y=0.1010369),
                Point(x=0.2156863, y=0.1403003),
                Point(x=0.2509804, y=0.1789547),
                Point(x=0.2862745, y=0.2205992),
                Point(x=0.3176471, y=0.2599225),
                Point(x=0.3490196, y=0.3011572),
                Point(x=0.3803922, y=0.3439884),
                Point(x=0.4117647, y=0.3880444),
                Point(x=0.4431373, y=0.4329080),
                Point(x=0.4745098, y=0.4781301),
                Point(x=0.5058824, y=0.5230899),
                Point(x=0.5372549, y=0.5670175),
                Point(x=0.5686275, y=0.6093478),
                Point(x=0.6000000, y=0.6497036),
                Point(x=0.6352941, y=0.6924760),
                Point(x=0.6705882, y=0.7323663),
                Point(x=0.7058824, y=0.7694375),
                Point(x=0.7450980, y=0.8075524),
                Point(x=0.7843137, y=0.8427844),
                Point(x=0.8235294, y=0.8755376),
                Point(x=0.8666667, y=0.9091544),
                Point(x=0.9098039, y=0.9406235),
                Point(x=0.9529412, y=0.9701468),
                Point(x=0.9960784, y=0.9976210),
                Point(x=1.0000000, y=1.0000000),
            ],
        )
