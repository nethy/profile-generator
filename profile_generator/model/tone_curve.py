import math
from collections.abc import Callable
from functools import cache

from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants, lab
from profile_generator.model.color.space import srgb
from profile_generator.unit import Curve, Point


def get_srgb_flat(grey18: float) -> Curve:
    return _as_srgb(grey18, get_linear_flat)


def get_lab_flat(grey18: float) -> Curve:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve = get_linear_flat(linear_grey18)
    return lambda x: lab.from_xyz_lum(curve(lab.to_xyz_lum(x * 100))) / 100


def get_linear_flat(linear_grey18: float) -> Curve:
    return _get_hybrid_log_flat(linear_grey18)


@cache
def _get_hybrid_log_flat(linear_grey18: float) -> Curve:
    mid = Point(linear_grey18, constants.GREY18_LINEAR)
    flat_log = gamma.log_at(mid)
    flat_pow = gamma.power_at(mid)
    weight = lambda x: 2 * math.pow(x, 3) - 3 * math.pow(x, 2) + 1
    return lambda x: weight(x) * flat_log(x) + (1 - weight(x)) * flat_pow(x)


def _as_srgb(grey18: float, curve_supplier: Callable[[float], Curve]) -> Curve:
    linear_grey18 = srgb.inverse_gamma(grey18)
    curve = curve_supplier(linear_grey18)
    return lambda x: srgb.gamma(curve(srgb.inverse_gamma(x)))


def get_srgb_contrast(grey18: float, gradient: float) -> Curve:
    contrast = get_linear_contrast(srgb.inverse_gamma(grey18), gradient)
    return lambda x: srgb.gamma(contrast(srgb.inverse_gamma(x)))


def get_lab_contrast(linear_grey18: float, gradient: float) -> Curve:
    contrast = get_linear_contrast(linear_grey18, gradient)
    return lambda x: lab.from_xyz_lum(contrast(lab.to_xyz_lum(x * 100))) / 100


def get_linear_contrast(gradient: float) -> Curve:
    return sigmoid.exponential(gradient)
