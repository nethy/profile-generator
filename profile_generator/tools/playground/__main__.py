# mypy: ignore-errors
# pylint: skip-file

import json
import math
from array import array
from email.mime import base
from functools import partial
from itertools import starmap
from operator import itemgetter

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


def lch_to_hsv(lab_color):
    return rgb.to_hsv(xyz.to_rgb(lab.to_xyz(lab.from_lch(lab_color)), SRGB))


def as_equalizer(cur, new):
    cur_h, new_h = cur[0], new[0]

    res_h = new_h - cur_h
    if res_h > 0.5:
        res_h -= 1
    elif res_h < -0.5:
        res_h += 1

    return raw_therapee.EqPoint(cur_h, (new_h - cur_h) / 2 + 0.5)


def lab_hue_rgb():
    shift = 3
    lab_hue = [(0, shift), (90, -shift), (150, shift), (240, -shift)]

    hsv_values = (
        (lch_to_hsv(x_lab), lch_to_hsv(y_lab))
        for x_lab, y_lab in (
            ([50, 25, x_hue], [50, 25, x_hue + mod_hue]) for x_hue, mod_hue in lab_hue
        )
    )

    equalizer_values = starmap(as_equalizer, hsv_values)

    print(
        raw_therapee.present_equalizer(
            sorted(list(equalizer_values), key=lambda eq_point: eq_point.x)
        )
    )


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

    lab_hue_rgb()
