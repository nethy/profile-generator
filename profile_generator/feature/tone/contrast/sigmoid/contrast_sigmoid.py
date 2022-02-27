import math
from collections.abc import Sequence
from functools import cache

from profile_generator.model import sigmoid, tone_curve
from profile_generator.model.color import constants
from profile_generator.model.color.space import srgb
from profile_generator.unit import Point, curve


@cache
def get_flat(grey18: float) -> Sequence[Point]:
    if _is_middle_grey(grey18):
        return []
    flat = tone_curve.get_lab_flat(grey18)
    return curve.as_points(flat)


@cache
def compensate_slope(grey18: float, slope: float) -> float:
    return tone_curve.compensate_gradient(grey18, slope)


@cache
def get_contrast(slope: float) -> Sequence[Point]:
    if math.isclose(slope, 1):
        return []
    contrast = tone_curve.get_lab_contrast(slope)
    return curve.as_points(contrast)


@cache
def get_tone_curve(grey18: float, slope: float) -> Sequence[Point]:
    if _is_middle_grey(grey18) and math.isclose(slope, 1):
        return []
    flat = tone_curve.get_lab_flat(grey18)
    contrast = tone_curve.get_lab_contrast(slope)
    return curve.as_points(lambda x: contrast(flat(x)))


@cache
def get_chromaticity_curve(slope: float) -> Sequence[Point]:
    if math.isclose(slope, 1):
        return []
    sigmoid_curve = sigmoid.algebraic(math.pow(slope, 0.75), 1)
    return curve.as_points(sigmoid_curve)


def _is_middle_grey(grey18: float) -> bool:
    return math.isclose(srgb.inverse_gamma(grey18), constants.GREY18_LINEAR)
