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
from profile_generator.unit import Curve, Line, Point, Strength, curve
from profile_generator.util import search


def normalize(point):
    diff = (point.y - point.x) * 0.5
    return Point(point.x - diff, point.y - diff)


def print_points(fn):
    for x, y in curve.as_points(fn):
        print_point(x, y)


def print_point(x, y):
    print(f"{x:.7f} {y:.7f}")


def find_x(fn, y):
    return search.jump_search(0, 1, fn, y)


def fn_diff(a, b):
    return sum((a(i) - b(i) for i in (0.5 + 0.5 * i / 100 for i in range(101))))


def naive_flat(midtone):
    shadow = Line.from_points(Point(0, 0), midtone)
    highlight = Line.from_points(midtone, Point(1, 1))
    return lambda x: shadow.get_y(x) if x < midtone.x else highlight.get_y(x)


if __name__ == "__main__":
    # grey = SRGB.gamma(SRGB.inverse_gamma(87.975 / 255) / 2) * 255
    # print_points(contrast_sigmoid.calculate(106.845, 1.85))
    # print_points(contrast_sigmoid.contrast(87.30522037562211 / 255, 1.85))
    # print_points(contrast_sigmoid.flat(80.86382712430665 / 255))
    # print_points(contrast_sigmoid.contrast(80.86382712430665 / 255, 1.85))
    # print_points(contrast_sigmoid.calculate(64.515, 1))
    # pass

    contrast = sigmoid.algebraic(2, 2)
    hl_ref = contrast(0.55)
    print(hl_ref)
    sh_ref = search.jump_search(
        1e-3, 1e3, lambda c: sigmoid.algebraic(2, c)(0.75), 0.825
    )
    print(sh_ref)
