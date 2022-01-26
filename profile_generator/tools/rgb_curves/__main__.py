import math

from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.linalg import Vector
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_BLACK = Point(0, 0)
_WHITE = Point(1, 1)


def main() -> None:
    shadow = color_vector(270, 3)
    midtone = color_vector(0, 0)
    highlight = color_vector(90, 6)
    for name, value in zip(
        ("rCurve", "gCurve", "bCurve"), rgb_curves(shadow, midtone, highlight)
    ):
        print(f"{name}=1;{value}")


def color_vector(degree: float, length: float) -> list[float]:
    radians = math.radians(degree)
    return [math.cos(radians) * length, math.sin(radians) * length]


def rgb_curves(
    shadow_tint: list[float], midtone_tint: list[float], highlight_tint: list[float]
) -> list[str]:
    black = [0.0, 0.0, 0.0]
    shadow = [25.0] + shadow_tint
    midtone = [50.0] + midtone_tint
    highlight = [75.0] + highlight_tint
    white = [100.0, 0.0, 0.0]
    tones = interpolate([black, shadow, midtone, highlight, white])
    rgbs = [lab_to_rgb(tone) for tone in tones]
    refs = [srgb_luminance(tone[0]) for tone in tones]
    rgb_points = [
        [Point(*ref_rgb_value) for ref_rgb_value in zip(refs, rgb_values)]
        for rgb_values in zip(*rgbs)
    ]
    return [raw_therapee.present_curve(points) for points in rgb_points]


def interpolate(items: list[Vector]) -> list[Vector]:
    result: list[list[float]] = []
    for i, item in enumerate(items):
        result.append(item)
        if i + 1 < len(items):
            interpolated = [(a + b) / 2 for a, b in zip(items[i], items[i + 1])]
            result.append(interpolated)
    return result


def lab_to_rgb(color: Vector) -> Vector:
    return xyz.to_rgb(lab.to_xyz(color), SRGB)


def srgb_luminance(lab_luminance: float) -> float:
    return SRGB.gamma(lab.to_xyz([lab_luminance, 0, 0])[1])


def ratios(color: Vector) -> list[float]:
    ref = max(color)
    return [i / ref for i in color]


if __name__ == "__main__":
    main()
