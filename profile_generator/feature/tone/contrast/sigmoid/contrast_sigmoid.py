from collections.abc import Sequence
from functools import cache

from profile_generator.model import spline, tone_curve
from profile_generator.unit import Point


@cache
def flat(grey18: float) -> Sequence[Point]:
    curve = tone_curve.flat(grey18)
    return spline.fit(curve)


@cache
def contrast(grey18: float, slope: float) -> Sequence[Point]:
    curve = tone_curve.contrast(grey18, slope)
    return spline.fit(curve)
