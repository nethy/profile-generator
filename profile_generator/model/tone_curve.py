import math
from functools import cache

from profile_generator.model import gamma, interpolation, sigmoid
from profile_generator.model.color import constants, lab
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Curve, Point


def get_rgb_flat(linear_grey18: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    return _as_rgb(flat)


def get_lab_flat(linear_grey18: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    return _as_lab(flat)


@cache
def get_linear_flat(linear_grey18: float) -> Curve:
    mid = Point(linear_grey18, constants.GREY18_LINEAR)
    shadow = gamma.log_at(mid)
    highlight = gamma.power_at(mid)
    return interpolation.interpolate(shadow, highlight, interpolation.geometric)


def _as_rgb(linear_curve: Curve) -> Curve:
    return lambda x: SRGB.gamma(linear_curve(SRGB.inverse_gamma(x)))


def _as_lab(linear_curve: Curve) -> Curve:
    return lambda x: lab.from_xyz_lum(linear_curve(lab.to_xyz_lum(x * 100))) / 100


def get_rgb_contrast(gradient: float) -> Curve:
    contrast = get_linear_contrast(gradient)
    return _as_rgb(contrast)


def get_lab_contrast(gradient: float) -> Curve:
    contrast = get_linear_contrast(gradient)
    return _as_lab(contrast)


@cache
def get_linear_contrast(gradient: float) -> Curve:
    shift_x = gamma.power_at(Point(constants.GREY18_LINEAR, 0.5))
    shift_y = gamma.power_at(Point(0.5, constants.GREY18_LINEAR))

    offset = math.log2(gradient) / 4
    shadow = sigmoid.exponential(gradient)
    highlight = sigmoid.exponential(gradient - offset)

    contrast = interpolation.interpolate(
        shadow, highlight, interpolation.geometric, 0.5, 1
    )

    return lambda x: shift_y(contrast(shift_x(x)))


def get_srgb(linear_grey18: float, slope: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    contrast = get_linear_contrast(slope)
    return _as_rgb(lambda x: contrast(flat(x)))


def get_lab(linear_grey18: float, slope: float) -> Curve:
    flat = get_linear_flat(linear_grey18)
    contrast = get_linear_contrast(slope)
    return _as_lab(lambda x: contrast(flat(x)))
