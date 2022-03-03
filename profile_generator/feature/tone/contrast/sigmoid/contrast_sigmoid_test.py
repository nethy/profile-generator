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
                Point(x=0.0322581, y=0.0437937),
                Point(x=0.0645161, y=0.0934556),
                Point(x=0.0967742, y=0.1468449),
                Point(x=0.1290323, y=0.1979940),
                Point(x=0.1612903, y=0.2473712),
                Point(x=0.1935484, y=0.2952913),
                Point(x=0.2258065, y=0.3419799),
                Point(x=0.2580645, y=0.3876054),
                Point(x=0.2903226, y=0.4322985),
                Point(x=0.3225806, y=0.4761630),
                Point(x=0.3548387, y=0.5189401),
                Point(x=0.3870968, y=0.5582107),
                Point(x=0.4193548, y=0.5942106),
                Point(x=0.4516129, y=0.6275826),
                Point(x=0.4838710, y=0.6587864),
                Point(x=0.5161290, y=0.6881635),
                Point(x=0.5483871, y=0.7159758),
                Point(x=0.5806452, y=0.7424292),
                Point(x=0.6129032, y=0.7676888),
                Point(x=0.6451613, y=0.7918893),
                Point(x=0.6774194, y=0.8151425),
                Point(x=0.7096774, y=0.8375421),
                Point(x=0.7419355, y=0.8591675),
                Point(x=0.7741935, y=0.8800869),
                Point(x=0.8064516, y=0.9003591),
                Point(x=0.8387097, y=0.9200354),
                Point(x=0.8709677, y=0.9391608),
                Point(x=0.9032258, y=0.9577751),
                Point(x=0.9354839, y=0.9759133),
                Point(x=0.9677419, y=0.9936071),
                Point(x=1.0000000, y=1.0108845),
            ],
        )

    def test_get_contrast(self) -> None:
        self.assertEqual(
            get_contrast(_SLOPE),
            [
                Point(x=0.0000000, y=0.0000000),
                Point(x=0.0322581, y=0.0029318),
                Point(x=0.0645161, y=0.0066290),
                Point(x=0.0967742, y=0.0113504),
                Point(x=0.1290323, y=0.0174585),
                Point(x=0.1612903, y=0.0254640),
                Point(x=0.1935484, y=0.0360885),
                Point(x=0.2258065, y=0.0503427),
                Point(x=0.2580645, y=0.0696078),
                Point(x=0.2903226, y=0.0956729),
                Point(x=0.3225806, y=0.1306180),
                Point(x=0.3548387, y=0.1763767),
                Point(x=0.3870968, y=0.2338910),
                Point(x=0.4193548, y=0.3021876),
                Point(x=0.4516129, y=0.3782187),
                Point(x=0.4838710, y=0.4580307),
                Point(x=0.5161290, y=0.5385711),
                Point(x=0.5483871, y=0.6165987),
                Point(x=0.5806452, y=0.6878482),
                Point(x=0.6129032, y=0.7496975),
                Point(x=0.6451613, y=0.8014155),
                Point(x=0.6774194, y=0.8436244),
                Point(x=0.7096774, y=0.8776186),
                Point(x=0.7419355, y=0.9048598),
                Point(x=0.7741935, y=0.9267032),
                Point(x=0.8064516, y=0.9442932),
                Point(x=0.8387097, y=0.9585493),
                Point(x=0.8709677, y=0.9701912),
                Point(x=0.9032258, y=0.9797755),
                Point(x=0.9354839, y=0.9877307),
                Point(x=0.9677419, y=0.9943871),
                Point(x=1.0000000, y=1.0000000),
            ],
        )
