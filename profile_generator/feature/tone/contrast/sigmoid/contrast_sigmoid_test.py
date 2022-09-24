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
                Point(x=0.0235294, y=0.0452095),
                Point(x=0.0549020, y=0.0896194),
                Point(x=0.0862745, y=0.1309024),
                Point(x=0.1176471, y=0.1721854),
                Point(x=0.1490196, y=0.2134684),
                Point(x=0.1803922, y=0.2547513),
                Point(x=0.2117647, y=0.2960343),
                Point(x=0.2431373, y=0.3373173),
                Point(x=0.2745098, y=0.3786003),
                Point(x=0.3058824, y=0.4198833),
                Point(x=0.3372549, y=0.4611662),
                Point(x=0.3725490, y=0.5043168),
                Point(x=0.4078431, y=0.5434588),
                Point(x=0.4431373, y=0.5802186),
                Point(x=0.4823529, y=0.6189074),
                Point(x=0.5215686, y=0.6556927),
                Point(x=0.5607843, y=0.6908075),
                Point(x=0.6000000, y=0.7244105),
                Point(x=0.6392157, y=0.7566194),
                Point(x=0.6823529, y=0.7905495),
                Point(x=0.7254902, y=0.8230070),
                Point(x=0.7686275, y=0.8540788),
                Point(x=0.8117647, y=0.8838417),
                Point(x=0.8549020, y=0.9123645),
                Point(x=0.8980392, y=0.9397105),
                Point(x=0.9411765, y=0.9659384),
                Point(x=0.9882353, y=0.9933395),
                Point(x=1.0000000, y=1.0000000),
            ],
        )

    def test_get_contrast(self) -> None:
        self.assertEqual(
            get_contrast(_SLOPE),
            [
                Point(x=0.0000000, y=0.0000000),
                Point(x=0.0509804, y=0.0130608),
                Point(x=0.0980392, y=0.0378278),
                Point(x=0.1372549, y=0.0691626),
                Point(x=0.1764706, y=0.1040913),
                Point(x=0.2156863, y=0.1427561),
                Point(x=0.2509804, y=0.1807929),
                Point(x=0.2862745, y=0.2218339),
                Point(x=0.3215686, y=0.2656971),
                Point(x=0.3529412, y=0.3068053),
                Point(x=0.3843137, y=0.3495871),
                Point(x=0.4156863, y=0.3936540),
                Point(x=0.4470588, y=0.4385527),
                Point(x=0.4784314, y=0.4837199),
                Point(x=0.5098039, y=0.5278180),
                Point(x=0.5411765, y=0.5702048),
                Point(x=0.5725490, y=0.6107408),
                Point(x=0.6078431, y=0.6540914),
                Point(x=0.6431373, y=0.6950868),
                Point(x=0.6784314, y=0.7338005),
                Point(x=0.7137255, y=0.7703308),
                Point(x=0.7529412, y=0.8084942),
                Point(x=0.7921569, y=0.8442584),
                Point(x=0.8313725, y=0.8777832),
                Point(x=0.8705882, y=0.9092243),
                Point(x=0.9137255, y=0.9415802),
                Point(x=0.9568627, y=0.9717810),
                Point(x=1.0000000, y=1.0000000),
            ],
        )
