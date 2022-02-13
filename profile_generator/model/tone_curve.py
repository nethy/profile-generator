import math

from profile_generator.model import gamma, sigmoid
from profile_generator.model.color import constants
from profile_generator.model.color.space import srgb
from profile_generator.unit import Curve, Point


def flat(grey18: float) -> Curve:
    return _flat(grey18)[0]


def _flat(grey18: float) -> tuple[Curve, Curve]:
    linear_midtone = Point(srgb.inverse_gamma(grey18), constants.GREY18_LINEAR)
    log = gamma.log_at(linear_midtone)
    log_derivative = gamma.log_derivative_at(linear_midtone)
    power = gamma.power_at(linear_midtone)
    power_derivative = gamma.power_derivative_at(linear_midtone)
    weight = gamma.algebraic_at(linear_midtone, 1)
    return _to_srgb_cruve(
        lambda x: (1 - weight(x)) * log(x) + weight(x) * power(x),
        lambda x: (1 - weight(x)) * log_derivative(x) + weight(x) * power_derivative(x),
    )


def _to_srgb_cruve(fn: Curve, derivative: Curve) -> tuple[Curve, Curve]:
    return (
        lambda x: srgb.gamma(fn(srgb.inverse_gamma(x))),
        lambda x: srgb.gamma_derivative(fn(srgb.inverse_gamma(x)))
        * derivative(srgb.inverse_gamma(x))
        * srgb.inverse_gamma_derivative(x),
    )


def contrast(grey18: float, gradient: float) -> Curve:
    _, derivative = _flat(grey18)
    corrected_gradient = gradient / derivative(grey18) + 1 - 1 / derivative(grey18)
    return _contrast(corrected_gradient)


def _contrast(gradient: float) -> Curve:
    if math.isclose(gradient, 1):
        return lambda x: x
    shadow = sigmoid.algebraic(gradient, 2.5)
    highlight = sigmoid.algebraic(gradient, 2)
    curve = lambda x: shadow(x) if x < 0.5 else highlight(x)
    shift_x = gamma.power_at(Point(constants.GREY18_SRGB, 0.5))
    shift_y = gamma.power_at(Point(0.5, constants.GREY18_SRGB))
    return lambda x: shift_y(curve(shift_x(x)))
