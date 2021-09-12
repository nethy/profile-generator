# mypy: ignore-errors
# pylint: skip-file

from profile_generator.feature.tone.contrast.bezier import contrast_bezier
from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _EV_COMP,
    _GAMMA,
    _GREY18,
    _OFFSETS,
)
from profile_generator.model import faded, gamma, linalg, sigmoid, spline
from profile_generator.model.color import constants, lab, rgb, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.color_chart import ColorChart
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point, Strength

if __name__ == "__main__":
    points = spline.fit(faded.curve(24 / 255, 0.1))
    for x, y in points:
        print(f"{x:.6f} {y:.6f}")
    print(raw_therapee.present_curve([Point(x, y) for x, y in points]))
