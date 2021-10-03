from collections.abc import Callable, Sequence

from profile_generator.feature.tone.contrast.sigmoid.schema import highlight
from profile_generator.model import linalg, sigmoid, spline
from profile_generator.model.color import lab, rgb, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.linalg import Vector
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point


def main() -> None:
    shadow = [0, -6]
    highlight = [0, 6]
    for name, value in zip(
        ("rCurve", "gCurve", "bCurve"), rgb_curves(shadow, highlight)
    ):
        print(f"{name}=1;{value}")


def rgb_curves(
    shadow_tint: tuple[float, float], highlight_tint: tuple[float, float]
) -> Sequence[str]:
    shadow = [50] + shadow_tint
    highlight = [50] + highlight_tint
    shadow_rgb = lab_to_rgb(shadow)
    highlight_rgb = lab_to_rgb(highlight)
    shadow_ratios = [1 / a for a in ratios(shadow_rgb)]
    highlight_ratios = ratios(highlight_rgb)
    shadow_curves = [sigmoid.contrast_curve_exp(g) for g in shadow_ratios]
    highlight_curves = [sigmoid.contrast_curve_exp(g) for g in highlight_ratios]
    weight = sigmoid.contrast_curve_exp(8)
    rgb_points = [
        spline.fit(lambda x: (1 - weight(x)) * s(x) + weight(x) * h(x))
        for s, h in zip(shadow_curves, highlight_curves)
    ]
    return [
        raw_therapee.present_curve((Point(x, y) for x, y in points))
        for points in rgb_points
    ]


def lab_to_rgb(color: Vector) -> Vector:
    return xyz.to_rgb(lab.to_xyz(color), SRGB)


def ratios(color: Vector) -> Sequence[float]:
    ref = max(color)
    return [i / ref for i in color]


if __name__ == "__main__":
    main()
