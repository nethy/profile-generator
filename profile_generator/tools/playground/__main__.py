# mypy: ignore-errors
# pylint: skip-file

import json
import math
from array import array
from email.mime import base
from functools import partial

from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _GREY18,
    _SLOPE,
)
from profile_generator.model import bezier, gamma, linalg, sigmoid, spline, tone_curve
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


def print_points(points):
    for x, y in points:
        print_point(x, y)


def print_point(x, y):
    print(f"{x:.7f} {y:.7f}")


def find_x(fn, y):
    return search.jump_search(0, 1, fn, y)


def fn_diff(a, b):
    return (
        sum((abs(a(i) - b(i)) for i in (0.5 + 0.5 * i / 255 for i in range(256)))) / 256
    )


def naive_flat(midtone):
    shadow = Line.from_points(Point(0, 0), midtone)
    highlight = Line.from_points(midtone, Point(1, 1))
    return lambda x: shadow.get_y(x) if x < midtone.x else highlight.get_y(x)


CURVE_LENGTH = constants.GREY18_LINEAR / 2
BLACK = Point(0, 0)
WHITE = Point(1, 1)


def bezier_flat(midtone):
    shadow = Line.from_points(BLACK, midtone)
    highlight = Line.from_points(midtone, WHITE)
    sh_ratio = min(CURVE_LENGTH / midtone.distance(BLACK), 1)
    curve_start = Point(
        midtone.x - midtone.x * sh_ratio, midtone.y - midtone.y * sh_ratio
    )
    hl_ratio = min(CURVE_LENGTH / midtone.distance(WHITE), 1)
    curve_end = Point(
        midtone.x + (WHITE.x - midtone.x) * hl_ratio,
        midtone.y + (WHITE.y - midtone.y) * hl_ratio,
    )
    transition = bezier.curve([(curve_start, 1), (midtone, 1), (curve_end, 1)])
    print(curve_start, midtone, curve_end)
    print(curve_start.distance(midtone), midtone.distance(curve_end))
    return (
        lambda x: shadow.get_y(x)
        if x < curve_start.x
        else transition(x)
        if x < curve_end.x
        else highlight.get_y(x)
    )


RATIO = 0.25


def bezier_hl_flat(midtone):
    shadow = Line.from_points(BLACK, midtone)
    hl_control = Point(
        midtone.x + (shadow.get_x(1) - midtone.x) * RATIO,
        midtone.y + (1 - midtone.y) * RATIO,
    )
    highlight = bezier.curve([(midtone, 1), (hl_control, 1), (WHITE, 1)])
    return lambda x: shadow.get_y(x) if x < midtone.x else highlight(x)


def spline_flat(midtone):
    c = midtone.gradient
    a = (1 - midtone.y) / (1 - midtone.y) - 2 + c
    b = 1 - a - c
    return lambda x: c * x if x < midtone.x else a * x * x * x + b * x * x + c * x


def to_srgb(fn):
    return lambda x: SRGB.gamma(fn(SRGB.inverse_gamma(x)))


def midtone_pass(curve):
    shadow_line = Line.from_points(Point(0.1, 0), Point(0.4, 1))
    highlight_line = Line.from_points(Point(0.6, 1), Point(0.9, 0))
    mask_curve = (
        lambda x: 0
        if x < 0.1
        else shadow_line.get_y(x)
        if x < 0.4
        else 1
        if x < 0.6
        else highlight_line.get_y(x)
        if x < 0.9
        else 0
    )
    return lambda x: mask_curve(x) * curve(x) + (1 - mask_curve(x)) * x


if __name__ == "__main__":
    # grey = SRGB.gamma(SRGB.inverse_gamma(87.975 / 255) / 2) * 255
    # print_points(contrast_sigmoid.get_tone_curve(106.845 / 255, 1.85))
    # print_points(contrast_sigmoid.get_tone_curve(87.30522037562211 / 255, 1))
    # print_points(contrast_sigmoid.flat(80.86382712430665 / 255))
    # print_points(contrast_sigmoid.get_tone_curve(80.86382712430665 / 255, 1.5))
    # print_points(contrast_sigmoid.get_tone_curve(63.189134638121 / 255, 2))

    # print_points(tone_curve._get_spline_flat(0.05))

    # contrast_curve = sigmoid.algebraic(math.pow(2, 0.25), math.sqrt(2))
    # print_points(
    #     midtone_pass(contrast_curve),
    # )

    # fn = spline.interpolate([(0, 0), (0.1, 0.09), (0.32, 0.43), (0.66, 0.87), (1, 1)])
    # linear_fn = lambda x: fn(SRGB.inverse_gamma(x))

    # target = SRGB.inverse_gamma(0.9)
    # print(target)
    # print(search.jump_search(0, 1, linear_fn, target))

    grey18_d40 = 0.136
    grey18_d7000 = 0.096
    grey18_g80 = 0.082
    grey18_g9 = 0.05
    slope = 1.7

    print_points(curve.as_points(tone_curve.get_srgb_contrast(slope)))
