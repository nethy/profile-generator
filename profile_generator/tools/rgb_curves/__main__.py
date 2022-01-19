import math

from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.linalg import Vector
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point

_BLACK = Point(0, 0)
_WHITE = Point(1, 1)


def main() -> None:
    shadow = normalize([0, -1], 2)
    midtone = normalize([1, -1], 5)
    highlight = normalize([0, 1], 2)
    for name, value in zip(
        ("rCurve", "gCurve", "bCurve"), rgb_curves(shadow, midtone, highlight)
    ):
        print(f"{name}=1;{value}")


def normalize(tint: list[float], base: float) -> list[float]:
    correction = math.sqrt(math.pow(tint[0], 2) + math.pow(tint[1], 2)) / base
    return [i / correction for i in tint] if not math.isclose(correction, 0) else tint


def rgb_curves(
    shadow_tint: list[float], midtone_tint: list[float], highlight_tint: list[float]
) -> list[str]:
    shadow = [25.0] + shadow_tint
    midtone = [50.0] + midtone_tint
    highlight = [75.0] + highlight_tint
    shadow_rgb = lab_to_rgb(shadow)
    grey_rgb = lab_to_rgb(midtone)
    highlight_rgb = lab_to_rgb(highlight)
    shadow_ref, grey_ref, highlight_ref = (
        srgb_luminance(i) for i in (25.0, 50.0, 75.0)
    )
    rgb_points = [
        [
            _BLACK,
            Point(shadow_ref, s),
            Point(grey_ref, g),
            Point(highlight_ref, h),
            _WHITE,
        ]
        for s, g, h in zip(shadow_rgb, grey_rgb, highlight_rgb)
    ]
    return [raw_therapee.present_curve(points) for points in rgb_points]


def lab_to_rgb(color: Vector) -> Vector:
    return xyz.to_rgb(lab.to_xyz(color), SRGB)


def srgb_luminance(lab_luminance: float) -> float:
    return SRGB.gamma(lab.to_xyz([lab_luminance, 0, 0])[1])


def ratios(color: Vector) -> list[float]:
    ref = max(color)
    return [i / ref for i in color]


if __name__ == "__main__":
    main()
