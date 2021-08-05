# mypy: ignore-errors
# pylint: skip-file

from profile_generator.feature.tone.contrast.bezier import contrast_bezier
from profile_generator.feature.tone.contrast.sigmoid import contrast_sigmoid
from profile_generator.feature.tone.contrast.sigmoid.contrast_sigmoid_test import (
    _EV_COMP,
    _GAMMA,
    _HL_TONE_DEFAULT,
    _HL_TONE_MAX,
    _HL_TONE_MIN,
    _NEUTRAL5,
    _OFFSETS,
)
from profile_generator.unit import Point, Strength


def print_calculation(name, fn, *args, **kwargs):
    print(name)
    print(fn(*args, **kwargs))
    print()


if __name__ == "__main__":
    print_calculation(
        "test_calculate",
        contrast_sigmoid.calculate,
        _NEUTRAL5,
        _GAMMA,
        _HL_TONE_DEFAULT,
    )
    print_calculation(
        "test_calculate_with_tone_strength_max",
        contrast_sigmoid.calculate,
        _NEUTRAL5,
        _GAMMA,
        _HL_TONE_MAX,
    ),
    print_calculation(
        "test_calculate_with_tone_strength_min",
        contrast_sigmoid.calculate,
        _NEUTRAL5,
        _GAMMA,
        _HL_TONE_MIN,
    ),
    print_calculation(
        "test_calculate_with_offests",
        contrast_sigmoid.calculate,
        _NEUTRAL5,
        _GAMMA,
        _HL_TONE_DEFAULT,
        offsets=_OFFSETS,
    )
    print_calculation(
        "test_calculate_with_exposure_compensation",
        contrast_sigmoid.calculate,
        _NEUTRAL5,
        _GAMMA,
        _HL_TONE_DEFAULT,
        ev_comp=_EV_COMP,
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
