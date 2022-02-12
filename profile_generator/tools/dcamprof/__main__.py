import json

from profile_generator.model import gamma, spline
from profile_generator.model.color import constants
from profile_generator.model.color.space import SRGB
from profile_generator.unit import Point


def dcamprof_tone_curve(camera_grey18_linear: float) -> None:
    print(SRGB.gamma(camera_grey18_linear) * 255)
    curve = [
        [x, y]
        for x, y in spline.fit(
            gamma.log_at(Point(camera_grey18_linear, constants.GREY18_LINEAR))
        )
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
    dcamprof_tone_curve(0.082)


if __name__ == "__main__":
    main()
