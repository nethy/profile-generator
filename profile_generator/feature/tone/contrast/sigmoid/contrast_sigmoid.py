from profile_generator.model.sigmoid import approximate_brightness, curve
from profile_generator.unit import Point, Strength

MAX_CONTRAST = 16


def calculate(grey: Point, strength: Strength, sample_size: int) -> list[Point]:
    contrast = strength.value * MAX_CONTRAST
    brightness = approximate_brightness(grey, contrast)
    return list(
        map(
            lambda x: Point(x, curve(contrast, brightness, x)),
            (x / (sample_size - 1) for x in range(sample_size)),
        ),
    )
