# mypy: ignore-errors
# pylint: skip-file

import math

from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _BRIGHTNESS,
    _GREY18,
    _SLOPE,
)
from profile_generator.model import (
    bezier,
    gamma,
    limited,
    linalg,
    sigmoid,
    spline,
    tone_curve,
)
from profile_generator.model.color import constants, lab, rgb, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.color_chart import ColorChart
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Curve, Line, Point, Strength
from profile_generator.util import search


def normalize(point: Point) -> Point:
    diff = (point.y - point.x) * 0.5
    return Point(point.x - diff, point.y - diff)


def print_point(x, y):
    print(f"{x:.6f} {y:.6f}")


if __name__ == "__main__":
    # grey = SRGB.gamma(SRGB.inverse_gamma(87.975 / 255) / 2) * 255
    # for x, y in contrast_sigmoid.calculate(106.845, 1.6, 0.5):
    # for x, y in contrast_sigmoid.calculate(87.975, 2):
    # for x, y in contrast_sigmoid.calculate(82.365, 1):
    # print_point(x, y)

    # line = Line(0.5 / 0.125, 0)
    # curve = lambda x: tone_curve.algebraic_gamma(x, line.get_x(0.5), 0.5)(line.get_x(1))
    # exponent = search.jump_search(0.1, 100, curve, 0.8)
    # print(exponent, curve(exponent))
    # for x, y in spline.fit(tone_curve.algebraic_gamma(1, line.get_x(0.5), 0.5)):
    #     print_point(x, y)

    # for x, y in spline.fit(tone_curve.algebraic_gamma(1, 0.125, 0.5)):
    for x, y in spline.fit(
        tone_curve.curve(Point(87.975 / 255, constants.LUMINANCE_50_SRGB), 2)
    ):
        print_point(x, y)
