import json

from profile_generator.model import tone_curve
from profile_generator.model.color.space import SRGB
from profile_generator.unit import curve


def dcamprof_tone_curve(camera_grey18_linear: float) -> None:
    grey18 = SRGB.gamma(camera_grey18_linear)
    print(round(grey18 * 255, 12))
    flat_curve, _ = tone_curve.get_linear_flat(camera_grey18_linear)
    handles = [[round(x, 7), round(y, 7)] for x, y in curve.as_points(flat_curve, 64)]
    output = {
        "CurveType": "Spline",
        "CurveHandles": handles,
        "CurveMax": 1,
        "CurveGamma": 1,
    }
    print(json.dumps(output))
    print()


def main() -> None:
    # dcamprof_tone_curve(0.136)  # D40
    # dcamprof_tone_curve(0.096)  # D7000
    # dcamprof_tone_curve(0.050)  # G9
    dcamprof_tone_curve(0.082)  # G8x
    # pass


if __name__ == "__main__":
    main()
