# mypy: ignore-errors
# pylint: skip-file

import math

from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _BRIGHTNESS,
    _GREY18,
    _SLOPE,
)
from profile_generator.model import gamma, limited, linalg, sigmoid, spline
from profile_generator.model.color import constants, lab, rgb, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.color_chart import ColorChart
from profile_generator.model.type import Curve
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point, Strength

if __name__ == "__main__":
    # for x, y in contrast_sigmoid.calculate(87.975, 1.75):
    for x, y in contrast_sigmoid.calculate(82.365, 1.75):
        print(f"{x:.6f} {y:.6f}")
