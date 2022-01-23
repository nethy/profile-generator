import math
from collections.abc import Sequence
from functools import cache

from profile_generator.model import spline, tone_curve
from profile_generator.model.color import rgb
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Point


@cache
def calculate(
    grey18: float,
    slope: float,
) -> Sequence[Point]:
    normalized_grey18 = rgb.normalize_value(grey18)
    _curve = tone_curve.filmic(normalized_grey18, slope)
    return spline.fit(_curve)


def _adjust_ev(value: float, ev: float) -> float:
    return SRGB.gamma(SRGB.inverse_gamma(value) * math.pow(2, ev))
