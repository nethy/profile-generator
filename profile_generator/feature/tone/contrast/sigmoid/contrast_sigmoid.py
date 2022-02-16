from collections.abc import Sequence
from functools import cache

from profile_generator.model import tone_curve
from profile_generator.unit import Point, curve


@cache
def flat(grey18: float) -> Sequence[Point]:
    flat_curve = tone_curve.flat(grey18)
    return curve.as_points(flat_curve)


@cache
def contrast(grey18: float, slope: float) -> Sequence[Point]:
    contrast_curve = tone_curve.contrast(grey18, slope)
    return curve.as_points(contrast_curve)
