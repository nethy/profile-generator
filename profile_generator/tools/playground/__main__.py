# mypy: ignore-errors
# pylint: skip-file

import math

from profile_generator.feature.tone.contrast.bezier import contrast_bezier
from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _BRIGHTNESS,
    _GREY18,
    _SLOPE,
)
from profile_generator.model import faded, gamma, linalg, sigmoid, spline
from profile_generator.model.color import constants, lab, rgb, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.color_chart import ColorChart
from profile_generator.model.type import Curve
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point, Strength


def power_brightness(x: float, y: float) -> Curve:
    b = y * (x - 1) / x / (y - 1)
    a = (y - 1) / math.pow(x - 1, b)

    def _curve(val: float) -> float:
        if val < x:
            return y / x * val
        else:
            return a * math.pow(val - 1, b) + 1

    return _curve


if __name__ == "__main__":
    grey18 = 87.975 / 255
    # gradient = 1
    # contrast_curve = sigmoid.contrast_curve_exp(gradient)
    # knots = (
    #     [(i * grey18 / 5, i * 10) for i in range(5)]
    #     + [(grey18 + i * (1 - grey18) / 5, 50 + i * 10) for i in range(5)]
    #     + [(1, 100)]
    # )
    # curve = [(x, contrast_curve(y / 100) * 100) for x, y in knots]
    # curve = [(x, SRGB.gamma(lab.to_xyz([y, 0, 0])[1])) for x, y in curve]
    # for x, y in knots:
    #     print(f"{x:.6f} {y:.6f}")
    # print()
    # for x, y in curve:
    #     print(f"{x:.6f} {y:.6f}")
    # print()
    # for x, y in spline.fit(
    #     gamma.piecewise(grey18, constants.MIDDLE_GREY_LUMINANCE_SRGB)[0]
    # ):
    #     print(f"{x:.6f} {y:.6f}")
    # print()
    # for x, y in contrast_sigmoid.calculate(87.975, 1.75):
    for x, y in contrast_sigmoid.calculate(82.365, 1.75, 1):
        print(f"{x:.6f} {y:.6f}")

    # gx = 0.25
    # gy = 0.5

    # for x, y in spline.fit(gamma.linear(gx, gy)[0]):
    #     print(f"{x:.6f} {y:.6f}")
    # print()
    # for x, y in spline.fit(power_brightness(gx, gy)):
    #     print(f"{x:.6f} {y:.6f}")
