import json
from typing import Any

from profile_generator.model import tone_curve
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Curve, curve


def main() -> None:
    # dcamprof_tone_curve(0.136)  # D40
    # dcamprof_tone_curve(0.096)  # D7000
    # dcamprof_tone_curve(0.082)  # G8x
    # dcamprof_tone_curve(0.050)  # G9
    pass


def dcamprof_tone_curve(camera_grey18_linear: float) -> None:
    grey18 = SRGB.gamma(camera_grey18_linear)

    print(round(grey18 * 255, 12))

    flat_curve = tone_curve.get_linear_flat(camera_grey18_linear)
    contrast_curve = tone_curve.get_linear_contrast(camera_grey18_linear, 1.5)
    flat = to_markup(flat_curve)
    standard = to_markup(lambda x: contrast_curve(flat_curve(x)))

    print("Writing flat.json")
    write_file("flat.json", flat)

    print("Writing standard.json")
    write_file("standard.json", standard)
    print()


def to_markup(c: Curve) -> dict[str, Any]:
    points = [[round(x, 7), round(y, 7)] for x, y in curve.as_fixed_points(c)]
    return {
        "CurveType": "Spline",
        "CurveHandles": points,
        "CurveMax": 1,
        "CurveGamma": 1,
    }


def write_file(file_name: str, content: dict[str, Any]) -> None:
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
