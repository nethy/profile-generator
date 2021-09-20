# mypy: ignore-errors
# pylint: skip-file

from profile_generator.feature.tone.contrast.bezier import contrast_bezier
from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _BRIGHTNESS,
    _GREY18,
    _SLOPE,
)
from profile_generator.model import gamma, linalg, sigmoid, spline
from profile_generator.model.color import lab, rgb, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.color_chart import ColorChart
from profile_generator.unit import Point, Strength


def print_calculation(name, fn, *args, **kwargs):
    print(name)
    result = fn(*args, **kwargs)
    if isinstance(result, list):
        print("[")
        for item in result:
            print(f"  {item},")
        print("]")
    else:
        print(result)
    print()


if __name__ == "__main__":
    print_calculation(
        "test_calculate",
        contrast_sigmoid.calculate,
        _GREY18,
        _SLOPE,
    )
    print_calculation(
        "test_base_controls_brightness",
        contrast_sigmoid.calculate,
        _GREY18,
        _SLOPE,
        _BRIGHTNESS,
    )
    print_calculation(
        "test_calculate_when_strength_is_less_than_1",
        contrast_bezier.calculate,
        Point(87 / 255, 119 / 255),
        Strength(0.2),
        (2, 1),
    )
    print_calculation(
        "test_calculate_when_strength_is_1",
        contrast_bezier.calculate,
        Point(0.5, 0.5),
        Strength(1),
        (2, 1),
    )
