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
    # for x, y in contrast_sigmoid.calculate(106.845, 1.6):
    for x, y in contrast_sigmoid.calculate(87.975, 1.7):
        # for x, y in contrast_sigmoid.calculate(82.365, 1.7):
        # for x, y in contrast_sigmoid.calculate(64.515, 1.7):
        print_point(x, y)
