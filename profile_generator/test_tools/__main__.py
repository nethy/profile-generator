# mypy: ignore-errors
# pylint: skip-file

from profile_generator.feature.colors.profile import marshaller as colors_marshaller
from profile_generator.feature.tone.contrast.bezier import contrast_bezier
from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _GREY,
    _OFFSETS,
    _STRENGTH,
)
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point, Strength


def print_calculation(name, fn, *args):
    print(name)
    print(fn(*args))
    print()


if __name__ == "__main__":
    print_calculation(
        "test_vibrance", colors_marshaller.get_profile_args, {"vibrance": 50}
    )
    print_calculation("test_calculate", contrast_sigmoid.calculate, _GREY, _STRENGTH)
    print_calculation(
        "test_calculate_with_offests",
        contrast_sigmoid.calculate,
        _GREY,
        _STRENGTH,
        _OFFSETS,
    )
    print_calculation(
        "test_calculate_with_hl_protection",
        contrast_sigmoid.calculate_with_hl_protection,
        _GREY,
        _STRENGTH,
    )
    print_calculation(
        "test_calculate_with_hl_protection_and_offests",
        contrast_sigmoid.calculate_with_hl_protection,
        _GREY,
        _STRENGTH,
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
    print_calculation(
        "negative_contrast",
        lambda *args: "\n".join(
            (raw_therapee._present_point(p) for p in contrast_sigmoid.calculate(*args))
        ),
        Point(81 / 255, 119 / 255),
        Strength(-1),
    )
