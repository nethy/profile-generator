import json

from profile_generator.model import spline, tone_curve
from profile_generator.model.color.space import SRGB


def dcamprof_tone_curve(camera_grey18_linear: float) -> None:
    grey18 = SRGB.gamma(camera_grey18_linear)
    print(round(grey18 * 255, 12))
    curve = [
        [round(x, 12), round(y, 12)] for x, y in spline.fit(tone_curve.flat(grey18))
    ]
    output = {
        "CurveType": "Spline",
        "CurveHandles": curve,
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
