import math
from collections.abc import Sequence
from functools import cache

from profile_generator.model import sigmoid, tone_curve
from profile_generator.model.color import constants
from profile_generator.unit import Point, curve


@cache
def get_flat(grey18: float) -> Sequence[Point]:
    if math.isclose(grey18, constants.GREY18_SRGB):
        return []
    flat = tone_curve.get_srgb_flat(grey18)
    return curve.as_points(flat)


@cache
def get_contrast(grey18: float, slope: float) -> Sequence[Point]:
    if math.isclose(slope, 1):
        return []
    contrast = tone_curve.get_srgb_contrast(grey18, slope)
    return curve.as_points(contrast)


@cache
def get_tone_curve(grey18: float, slope: float) -> Sequence[Point]:
    flat = tone_curve.get_srgb_flat(grey18)
    contrast = tone_curve.get_srgb_contrast(grey18, slope)
    return curve.as_points(lambda x: contrast(flat(x)))


@cache
def get_chromaticity_curve(slope: float) -> Sequence[Point]:
    if math.isclose(slope, 1):
        return []
    return curve.as_points(sigmoid.algebraic((1 + (slope - 1) / 2), 1))
