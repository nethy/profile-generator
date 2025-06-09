import math
from functools import cache

from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants, lab
from profile_generator.model.color.space import srgb
from profile_generator.unit import Curve, Point


def get_srgb_flat(linear_grey18: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    return _as_srgb(flat)


def get_lab_flat(linear_grey18: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    return _as_lab(flat)


@cache
def get_linear_flat(linear_grey18: float) -> Curve:
    mid = Point(linear_grey18, constants.GREY18_LINEAR)
    flat_log = gamma.log_at(mid)
    flat_pow = gamma.power_at(mid)
    weight = _get_linear_flat_weight(linear_grey18)
    return lambda x: weight(x) * flat_log(x) + (1 - weight(x)) * flat_pow(x)


def _get_linear_flat_weight(linear_grey18: float) -> Curve:
    def _get_shift(linear_grey18: float) -> Curve:
        if linear_grey18 < 0.5:
            exp = math.log(1 - 0.5) / math.log(1 - linear_grey18)
            return lambda x: 1 - math.pow(1 - x, exp)
        else:
            exp = math.log(0.5) / math.log(linear_grey18)
            return lambda x: math.pow(x, exp)

    def _hermite_base(x: float) -> float:
        return 2 * math.pow(x, 3) - 3 * math.pow(x, 2) + 1

    shift = _get_shift(min(linear_grey18 * 2, 0.8))
    return lambda x: _hermite_base(shift(x))


def _as_srgb(linear_curve: Curve) -> Curve:
    return lambda x: srgb.gamma(linear_curve(srgb.inverse_gamma(x)))


def _as_lab(linear_curve: Curve) -> Curve:
    return lambda x: lab.from_xyz_lum(linear_curve(lab.to_xyz_lum(x * 100))) / 100


def get_srgb_contrast(gradient: float) -> Curve:
    contrast = get_linear_contrast(gradient)
    return _as_srgb(contrast)


def get_lab_contrast(gradient: float) -> Curve:
    contrast = get_linear_contrast(gradient)
    return _as_lab(contrast)


def get_linear_contrast(gradient: float) -> Curve:
    shift_x = gamma.power_at(Point(constants.GREY18_LINEAR, 0.5))
    shift_y = gamma.power_at(Point(0.5, constants.GREY18_LINEAR))
    contrast = sigmoid.exponential(gradient)
    return lambda x: shift_y(contrast(shift_x(x)))


def get_srgb(linear_grey18: float, slope: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    contrast = get_linear_contrast(slope)
    return _as_srgb(lambda x: contrast(flat(x)))


def get_lab(linear_grey18: float, slope: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    contrast = get_linear_contrast(slope)
    return _as_lab(lambda x: contrast(flat(x)))
