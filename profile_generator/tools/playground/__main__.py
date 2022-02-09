# mypy: ignore-errors
# pylint: skip-file

import json
import math
from cmath import exp
from colorsys import rgb_to_hsv
from functools import partial

from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
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
from profile_generator.model.color.space.prophoto import PROPHOTO
from profile_generator.model.color_chart import ColorChart
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Curve, Line, Point, Strength
from profile_generator.util import search


def normalize(point):
    diff = (point.y - point.x) * 0.5
    return Point(point.x - diff, point.y - diff)


def print_points(flat, contrast):
    for x, y in flat:
        print_point(x, y)
    print()
    for x, y in contrast:
        print_point(x, y)


def print_point(x, y):
    print(f"{x:.6f} {y:.6f}")


def find_x(fn, y):
    return search.jump_search(0, 1, fn, y)


def fn_diff(a, b):
    return sum((a(i) - b(i) for i in (0.5 + 0.5 * i / 100 for i in range(101))))


def naive_flat(midtone):
    shadow = Line.from_points(Point(0, 0), midtone)
    highlight = Line.from_points(midtone, Point(1, 1))
    return lambda x: shadow.get_y(x) if x < midtone.x else highlight.get_y(x)


def lum_to_srgb(luminance):
    return SRGB.gamma(lab.to_xyz([luminance, 0, 0])[1])


if __name__ == "__main__":
    # grey = SRGB.gamma(SRGB.inverse_gamma(87.975 / 255) / 2) * 255
    # print_points(contrast_sigmoid.calculate(106.845, 1.85))
    # print_points(*contrast_sigmoid.calculate(87.21, 1.85))
    # print_points(contrast_sigmoid.calculate(82.365, 1.7))
    # print_points(contrast_sigmoid.calculate(64.515, 1))

    # print(round(rgb.to_hsv(rgb.normalize(ColorChart.BLUE))[1] * 100, 1))
    # print(round(rgb.to_hsv(rgb.normalize(ColorChart.GREEN))[1] * 100, 1))
    # print(round(rgb.to_hsv(rgb.normalize(ColorChart.RED))[1] * 100, 1))
    middle_grey = lum_to_srgb(26.9)
    print(middle_grey * 255)
    curve = [
        [x * 255, y * 255]
        for x, y in spline.fit(
            gamma.log_at(Point(middle_grey, constants.LUMINANCE_50_SRGB))
        )
    ]
    output = {
        "CurveType": "Spline",
        "CurveHandles": curve,
        "CurveMax": 255,
        "CurveGamma": "sRGB",
    }
    print(json.dumps(output))
