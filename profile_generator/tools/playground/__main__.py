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
from profile_generator.unit import Curve, Point, Strength


def normalize(point: Point) -> Point:
    diff = (point.y - point.x) * 0.5
    return Point(point.x - diff, point.y - diff)


if __name__ == "__main__":
    # grey = SRGB.gamma(SRGB.inverse_gamma(87.975 / 255) / 2) * 255
    # for x, y in contrast_sigmoid.calculate(106.845, 1.6):
    # for x, y in contrast_sigmoid.calculate(87.975, 1.6, 2.5):
    # for x, y in contrast_sigmoid.calculate(82.365, 1.75):
    # print(f"{x:.6f} {y:.6f}")
    # for x, y in spline.fit(tone_curve.hybrid_gamma(0.125, 0.5)):
    #     print(f"{x:.6f} {y:.6f}")

    points = [(Point(0, 0), 1), (Point(0.25, 0.5), 2), (Point(1, 1), 1)]
    curve = lambda x: bezier.get_point_at(points, x)
    for x, y in (bezier.get_point_at(points, i / 14) for i in range(15)):
        print(f"{x:.6f} {y:.6f}")

    # shadow, midtone, highlight = 0, 2, -1
    # adjustments = [shadow + midtone * 0.5, midtone, highlight + midtone * 0.5]
    # refs = (0.25, 0.50, 0.75)
    # points = (
    #     Point(ref, ref + 0.01 * adjustment)
    #     for adjustment, ref in zip(adjustments, refs)
    # )
    # points = (normalize(p) for p in points)
    # print("0;0;" + raw_therapee.present_curve(points) + "1;1;")

    # base = sigmoid.contrast_curve_exp(1.5)
    # weight = sigmoid.contrast_curve_exp(2)

    # def _curve(x: float) -> float:
    #     if x < 0.5:
    #         return (1 - 2 * weight(x)) * base(x) + 2 * weight(x) * x
    #     else:
    #         return x

    # for x, y in spline.fit(_curve):
    #     print(f"{x:.6f} {y:.6f}")
