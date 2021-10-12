import math
from collections.abc import Sequence
from functools import cache

from profile_generator.model import spline
from profile_generator.model.color import constants, rgb
from profile_generator.model.color.space import SRGB
from profile_generator.model.tone_curve import (
    hybrid_gamma,
    hybrid_inverse_gamma,
    tone_curve_filmic,
)
from profile_generator.unit import Point


@cache
def calculate(
    grey18: float,
    slope: float,
    brightness: float = 0.0,
) -> Sequence[Point]:
    middle = _get_middle(grey18)
    gamma_fn = hybrid_inverse_gamma if brightness < 0 else hybrid_gamma
    brightness_curve = gamma_fn(
        rgb.normalize_value(grey18),
        _adjust_ev(rgb.normalize_value(grey18), brightness),
    )
    curve = tone_curve_filmic(middle, slope)
    return [Point(x, y) for x, y in spline.fit(lambda x: curve(brightness_curve(x)))]


def _get_middle(grey18: float) -> Point:
    in_lum = rgb.normalize_value(grey18)
    out_lum = constants.MIDDLE_GREY_LUMINANCE_SRGB
    return Point(in_lum, out_lum)


def _adjust_ev(value: float, ev: float) -> float:
    return SRGB.gamma(SRGB.inverse_gamma(value) * math.pow(2, ev))
