from collections.abc import Sequence
from functools import cache

from profile_generator.model import tone_curve
from profile_generator.model.color import constants
from profile_generator.unit import Point, curve
from profile_generator.unit.precision import equals


@cache
def get_flat(linear_grey18: float) -> Sequence[Point]:
    if equals(linear_grey18, constants.GREY18_LINEAR):
        return []
    flat = tone_curve.get_rgb_flat(linear_grey18)
    return curve.as_points(flat)


@cache
def get_contrast(slope: float) -> Sequence[Point]:
    if equals(slope, 1):
        return []
    contrast = tone_curve.get_rgb_contrast(slope)
    return curve.as_points(contrast)


@cache
def get_tone_curve(grey18: float, slope: float) -> Sequence[Point]:
    return curve.as_points(tone_curve.get_rgb(grey18, slope))
