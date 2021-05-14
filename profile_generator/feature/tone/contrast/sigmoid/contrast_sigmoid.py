from profile_generator.model.sigmoid import (
    contrast_slope,
    curve,
    curve_with_hl_protection,
    find_contrast_slope,
    find_curve_brightness,
)
from profile_generator.unit import PRECISION, Point, Strength

MAX_CONTRAST = 16


def calculate(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
    sample_size: int = 17,
) -> list[Point]:
    contrast = strength.value * MAX_CONTRAST
    contrast = _corrigate_contrast(contrast, offsets)
    brightness = find_curve_brightness(grey, contrast)
    return list(
        map(
            lambda x: Point(
                x,
                curve(contrast, brightness, x) * (offsets[1] - offsets[0]) + offsets[0],
            ),
            (x / (sample_size - 1) for x in range(sample_size)),
        ),
    )


def calculate_with_hl_protection(
    grey: Point,
    strength: Strength,
    offsets: tuple[float, float] = (0, 1),
    sample_size: int = 17,
) -> list[Point]:
    contrast = strength.value * MAX_CONTRAST
    contrast = _corrigate_contrast(contrast, offsets)
    brightness = find_curve_brightness(grey, contrast)
    return list(
        map(
            lambda x: Point(
                x,
                curve_with_hl_protection(contrast, brightness, x)
                * (offsets[1] - offsets[0])
                + offsets[0],
            ),
            (x / (sample_size - 1) for x in range(sample_size)),
        ),
    )


def _corrigate_contrast(c: float, offsets: tuple[float, float]) -> float:
    shadow, highlight = offsets
    if abs(1 - (highlight - shadow)) < PRECISION:
        return c
    slope = contrast_slope(c) / (highlight - shadow)
    return find_contrast_slope(slope)
