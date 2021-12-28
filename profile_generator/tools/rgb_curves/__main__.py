import math

from profile_generator.model import sigmoid, spline
from profile_generator.model.color import lab, xyz
from profile_generator.model.color.space import SRGB
from profile_generator.model.linalg import Vector
from profile_generator.model.view import raw_therapee
from profile_generator.unit import Point


def main() -> None:
    shadow = normalize([0, -1], 7)
    highlight = normalize([0, 1], 7)
    print(shadow, highlight)
    for name, value in zip(
        ("rCurve", "gCurve", "bCurve"), rgb_curves(shadow, highlight)
    ):
        print(f"{name}=1;{value}")


def normalize(tint: list[float], base: float) -> list[float]:
    correction = math.sqrt(math.pow(tint[0], 2) + math.pow(tint[1], 2)) / base
    return [i / correction for i in tint]


def rgb_curves(shadow_tint: list[float], highlight_tint: list[float]) -> list[str]:
    shadow = [50.0] + shadow_tint
    highlight = [50.0] + highlight_tint
    shadow_rgb = lab_to_rgb(shadow)
    highlight_rgb = lab_to_rgb(highlight)
    shadow_ratios = [1 / a for a in ratios(shadow_rgb)]
    highlight_ratios = ratios(highlight_rgb)
    shadow_curves = [sigmoid.algebraic(gradient, 2) for gradient in shadow_ratios]
    highlight_curves = [sigmoid.algebraic(gradient, 2) for gradient in highlight_ratios]
    mask = sigmoid.algebraic(8, 2)
    rgb_points = [
        spline.fit(
            lambda x: (1 - mask(x)) * s(x)  # pylint: disable=cell-var-from-loop
            + mask(x) * h(x)  # pylint: disable=cell-var-from-loop
        )
        for s, h in zip(shadow_curves, highlight_curves)
    ]
    return [
        raw_therapee.present_curve((Point(x, y) for x, y in points))
        for points in rgb_points
    ]


def lab_to_rgb(color: Vector) -> Vector:
    return xyz.to_rgb(lab.to_xyz(color), SRGB)


def ratios(color: Vector) -> list[float]:
    ref = max(color)
    return [i / ref for i in color]


if __name__ == "__main__":
    main()
