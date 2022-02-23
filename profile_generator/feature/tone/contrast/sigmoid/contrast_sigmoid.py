import math
from collections.abc import Sequence
from functools import cache

from profile_generator.model import sigmoid, tone_curve
from profile_generator.unit import Point, curve


@cache
def get_flat(grey18: float) -> Sequence[Point]:
    flat = tone_curve.get_lab_flat(grey18)
    return curve.as_points(flat)


@cache
def compensate_slope(grey18: float, slope: float) -> float:
    return tone_curve.compensate_gradient(grey18, slope)


@cache
def get_contrast(slope: float) -> Sequence[Point]:
    contrast = tone_curve.get_lab_contrast(slope)
    return curve.as_points(contrast)


@cache
def get_tone_curve(grey18: float, slope: float) -> Sequence[Point]:
    flat = tone_curve.get_lab_flat(grey18)
    contrast = tone_curve.get_lab_contrast(slope)
    return curve.as_points(lambda x: contrast(flat(x)))


@cache
def get_chromaticity_curve(slope: float) -> Sequence[Point]:
    sigmoid_curve = sigmoid.algebraic(math.pow(slope, 0.75), 1)
    return curve.as_points(sigmoid_curve)
