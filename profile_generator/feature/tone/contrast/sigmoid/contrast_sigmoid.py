import math
from collections.abc import Sequence
from functools import cache

from profile_generator.model import spline
from profile_generator.model.color import constants, rgb
from profile_generator.model.color.space import SRGB
from profile_generator.model.tone_curve import filmic
from profile_generator.unit import Point


@cache
def calculate(
    grey18: float,
    slope: float,
    brightness: float = 0.0,
) -> Sequence[Point]:
    normalized_grey18 = rgb.normalize_value(grey18)
    brightness_output = _adjust_ev(normalized_grey18, brightness)
    brightness_curve = filmic(Point(normalized_grey18, brightness_output), 1)
    middle = Point(normalized_grey18, constants.LUMINANCE_50_SRGB)
    _curve = filmic(middle, slope)
    return [Point(x, y) for x, y in spline.fit(lambda x: _curve(brightness_curve(x)))]


def _adjust_ev(value: float, ev: float) -> float:
    return SRGB.gamma(SRGB.inverse_gamma(value) * math.pow(2, ev))
