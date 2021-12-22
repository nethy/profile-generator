import math
from collections.abc import Sequence
from functools import cache

from profile_generator.model import spline
from profile_generator.model.color import constants, rgb
from profile_generator.model.color.space import SRGB
from profile_generator.model.tone_curve import algebraic_gamma, tone_curve_filmic
from profile_generator.unit import Point


@cache
def calculate(
    grey18: float,
    slope: float,
    brightness: float = 0.0,
) -> Sequence[Point]:
    normalized_grey18 = rgb.normalize_value(grey18)
    output = _adjust_ev(normalized_grey18, brightness)
    middle = _get_middle(normalized_grey18)
    brightness_curve = algebraic_gamma(
        2 / 3,
        normalized_grey18,
        output,
    )
    corrected_slope = _corrected_slope(middle, slope)
    curve = tone_curve_filmic(middle, corrected_slope)
    return [Point(x, y) for x, y in spline.fit(lambda x: curve(brightness_curve(x)))]


def _get_middle(in_lum: float) -> Point:
    out_lum = constants.MIDDLE_GREY_LUMINANCE_SRGB
    return Point(in_lum, out_lum)


def _adjust_ev(value: float, ev: float) -> float:
    return SRGB.gamma(SRGB.inverse_gamma(value) * math.pow(2, ev))


def _corrected_slope(middle: Point, slope: float) -> float:
    return (
        (slope - 1) * math.sqrt(middle.gradient) + middle.gradient
    ) / middle.gradient
