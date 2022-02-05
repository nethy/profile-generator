import json
import sys

from profile_generator.feature.colors.grading import grading
from profile_generator.model.view import raw_therapee
from profile_generator.util import file

TEMPLATE = """
[RGB Curves]
Enabled=true
LumaMode=false
rCurve={RGBCurvesRCurve}
gCurve={RGBCurvesGCurve}
bCurve={RGBCurvesBCurve}
"""

_DEFAULT = [0.0, 0.0, 0.0]

_OUTPUT_DIR = "profiles"


def main() -> None:
    raw_config = file.read_file(sys.argv[1])
    configuration = json.loads(raw_config)
    for name, config in configuration.items():
        global_hcl = config.get("global", _DEFAULT)
        shadow = config.get("shadow", _DEFAULT)
        midtone = config.get("midtone", _DEFAULT)
        highlight = config.get("highlight", _DEFAULT)

        curves = grading.rgb_curves(global_hcl, shadow, midtone, highlight)

        template_values = {
            template: raw_therapee.present_curve(
                raw_therapee.CurveType.STANDARD, points
            )
            for template, points in zip(
                ["RGBCurvesRCurve", "RGBCurvesGCurve", "RGBCurvesBCurve"],
                curves,
            )
        }

        template = TEMPLATE.format(**template_values)

        file.write_file(template, _OUTPUT_DIR, f"rgb-curves-{name}.pp3")

        print("Profile has been generated: " + name)


if __name__ == "__main__":
    main()
