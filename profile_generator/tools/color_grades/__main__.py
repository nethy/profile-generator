import json
import sys

from profile_generator.feature.colors.grading import toning
from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.util import file

TEMPLATE = """
[ColorToning]
Enabled={CTEnabled}
Method=LabRegions
Lumamode=true
Twocolor=Std
Redlow=0
Greenlow=0
Bluelow=0
Satlow=0
Balance=0
Sathigh=0
Redmed=0
Greenmed=0
Bluemed=0
Redhigh=0
Greenhigh=0
Bluehigh=0
Autosat=true
OpacityCurve=1;0;0.29999999999999999;0.34999999999999998;0;0.25;0.80000000000000004;0.34999999999999998;0.34999999999999998;0.69999999999999996;0.80000000000000004;0.34999999999999998;0.34999999999999998;1;0.29999999999999999;0;0;
ColorCurve=1;0.050000000000000003;0.62;0.25;0.25;0.58499999999999996;0.11;0.25;0.25;
SatProtectionThreshold=30
SaturatedOpacity=80
Strength=50
HighlightsColorSaturation=60;80;
ShadowsColorSaturation=80;208;
ClCurve=3;0;0;0.34999999999999998;0.65000000000000002;1;1;
Cl2Curve=3;0;0;0.34999999999999998;0.65000000000000002;1;1;
LabGridALow=0
LabGridBLow=0
LabGridAHigh=0
LabGridBHigh=0
LabRegionA_1={CTA1}
LabRegionB_1={CTB1}
LabRegionSaturation_1=0
LabRegionSlope_1=1
LabRegionOffset_1=0
LabRegionPower_1=1
LabRegionHueMask_1=0;
LabRegionChromaticityMask_1=0;
LabRegionLightnessMask_1=0;
LabRegionMaskBlur_1=0
LabRegionChannel_1=-1
LabRegionA_2={CTA2}
LabRegionB_2={CTB2}
LabRegionSaturation_2=0
LabRegionSlope_2=1
LabRegionOffset_2=0
LabRegionPower_2=1
LabRegionHueMask_2=0;
LabRegionChromaticityMask_2=0;
LabRegionLightnessMask_2=1;0.1666667;1;0.25;0.25;0.5;0;0.25;0.25;
LabRegionMaskBlur_2=0
LabRegionChannel_2=-1
LabRegionA_3={CTA3}
LabRegionB_3={CTB3}
LabRegionSaturation_3=0
LabRegionSlope_3=1
LabRegionOffset_3=0
LabRegionPower_3=1
LabRegionHueMask_3=0;
LabRegionChromaticityMask_3=0;
LabRegionLightnessMask_3=1;0.1666667;0;0.25;0.25;0.5;1;0.25;0.25;0.8333333;0;0.25;0.25;
LabRegionMaskBlur_3=0
LabRegionChannel_3=-1
LabRegionA_4={CTA4}
LabRegionB_4={CTB4}
LabRegionSaturation_4=0
LabRegionSlope_4=1
LabRegionOffset_4=0
LabRegionPower_4=1
LabRegionHueMask_4=0;
LabRegionChromaticityMask_4=0;
LabRegionLightnessMask_4=1;0.5;0;0.25;0.25;0.8333333;1;0.25;0.25;
LabRegionMaskBlur_4=0
LabRegionChannel_4=-1
LabRegionsShowMask=-1
"""

_DEFAULT = [0.0, 0.0, 0.0]

_OUTPUT_DIR = "profiles"


def main() -> None:
    raw_config = file.read_file(sys.argv[1])
    configuration = json.loads(raw_config)
    for name, config in configuration.items():
        profile_params = ProfileParams()
        profile_params.colors.grading.toning.parse(config)

        template_values = toning.generate(profile_params)

        template = TEMPLATE.format(**template_values)

        file.write_file(template, _OUTPUT_DIR, f"rgb-curves-{name}.pp3")

        print("Profile has been generated: " + name)


if __name__ == "__main__":
    main()
