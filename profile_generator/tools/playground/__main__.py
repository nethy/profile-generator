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


def print_eq_points(points):
    shoulder = 1 / 6
    print("ControlPoints")
    for p in points:
        print(round(p.x, 6), round(p.y, 6))
        print(round(shoulder, 6), round(shoulder, 6))


def find_x(fn, y):
    return search.jump_search(0, 1, fn, y)


def fn_diff(a, b):
    return (
        sum((abs(a(i) - b(i)) for i in (0.5 + 0.5 * i / 255 for i in range(256)))) / 256
    )


def lch_to_hsv(lab_color):
    return rgb.to_hsv(xyz.to_rgb(lab.to_xyz(lab.from_lch(lab_color)), SRGB))


def lab_hue_to_rgb_hue(HH):
    hr = 0.0

    if HH >= 0 and HH < 0.6:
        hr = 0.11666 * HH + 0.93
    elif HH >= 0.6 and HH < 1.4:
        hr = 0.1125 * HH - 0.0675
    elif HH >= 1.4 and HH < 2:
        hr = 0.2666 * HH - 0.2833
    elif HH >= 2 and HH < 3.14159:
        hr = 0.1489 * HH - 0.04785
    elif HH >= -3.14159 and HH < -2.8:
        hr = 0.23419 * HH + 1.1557
    elif HH >= -2.8 and HH < -2.3:
        hr = 0.16 * HH + 0.948
    elif HH >= -2.3 and HH < -0.9:
        hr = 0.12143 * HH + 0.85928
    elif HH >= -0.9 and HH < -0.1:
        hr = 0.2125 * HH + 0.94125
    elif HH >= -0.1 and HH < 0:
        hr = 0.1 * HH + 0.93

    if hr < 0.0:
        hr += 1.0
    elif hr > 1.0:
        hr -= 1.0

    return hr


def to_radians(degree):
    return round(math.radians(degree if degree < 180 else degree - 360), 5)


def lch_hue():
    shift = 6
    lab_hue = [(0, shift), (90, -shift), (180, shift), (270, -shift)]

    lab_hue_in_radians = starmap(
        lambda a, b: (to_radians(a), to_radians(a + b)), lab_hue
    )
    # print(list(lab_hue_in_radians))

    def as_equalizer(cur, new):
        return raw_therapee.EqPoint(lab_hue_to_rgb_hue(cur), (new - cur) / 1.7 + 0.5)

    equalizer_values = starmap(as_equalizer, lab_hue_in_radians)

    print_eq_points(sorted(list(equalizer_values), key=lambda eq_point: eq_point.x))


def lch_lightness():
    lab_lightness = [(45, 1.05), (225, 0.95)]

    lab_hue_in_radians = starmap(lambda a, b: (to_radians(a), b), lab_lightness)
    # print(list(lab_hue_in_radians))

    def as_equalizer(cur, new):
        result = 1
        if new > 1:
            result = (new - 1) / 6 + 0.5
        else:
            result = (new - 1) / 1.9 + 0.5
        return raw_therapee.EqPoint(lab_hue_to_rgb_hue(cur), result)

    equalizer_values = starmap(as_equalizer, lab_hue_in_radians)

    print_eq_points(sorted(list(equalizer_values), key=lambda eq_point: eq_point.x))


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
