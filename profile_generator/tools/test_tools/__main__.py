# mypy: ignore-errors
# pylint: skip-file

from profile_generator.feature.colors.schema import SCHEMA as color_schema
from profile_generator.feature.tone.contrast.bezier import contrast_bezier
from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _GAMMA,
    _GREY,
    _HL_PROTECTION,
    _OFFSETS,
)
from profile_generator.model import color_chart, colorspace, linalg, sigmoid, spline
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point, Strength


def print_calculation(name, fn, *args, **kwargs):
    print(name)
    print(fn(*args, **kwargs))
    print()


if __name__ == "__main__":
    print_calculation("test_vibrance", color_schema.process, {"vibrance": 50})
    print_calculation("test_calculate", contrast_sigmoid.calculate, _GREY, _GAMMA)
    print_calculation(
        "test_calculate_with_offests",
        contrast_sigmoid.calculate,
        _GREY,
        _GAMMA,
        offsets=_OFFSETS,
    )
    print_calculation(
        "test_calculate_with_hl_protection",
        contrast_sigmoid.calculate,
        _GREY,
        _GAMMA,
        _HL_PROTECTION,
    )
    print_calculation(
        "test_calculate_with_hl_protection_and_offests",
        contrast_sigmoid.calculate,
        _GREY,
        _GAMMA,
        _HL_PROTECTION,
        _OFFSETS,
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
