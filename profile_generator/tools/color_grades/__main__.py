import json
import sys

from profile_generator.feature.colors.grading import profile_generator
from profile_generator.main.profile_params import ProfileParams
from profile_generator.util import file

TEMPLATE = """
[RGB Curves]
Enabled={RGBCurvesEnabled}
LumaMode=false
rCurve={RGBCurvesRCurve}
gCurve={RGBCurvesGCurve}
bCurve={RGBCurvesBCurve}
"""

_OUTPUT_DIR = "profiles"


def main() -> None:
    raw_config = file.read_file(sys.argv[1])
    configuration = json.loads(raw_config)
    for name, config in configuration.items():
        profile_params = ProfileParams()
        profile_params.colors.grading.parse(config)

        template_values = profile_generator.generate(profile_params)

        template = TEMPLATE.format(**template_values)

        file.write_file(template, _OUTPUT_DIR, f"rgb-curves-{name}.pp3")

        print("Profile has been generated: " + name)


if __name__ == "__main__":
    main()
