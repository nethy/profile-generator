"""
Tonal ranges:
shadow:     0.16667 0.50000
midtone:    0.16667 0.50000 0.83333
highlight:  0.50000 0.83333


Bezier slope

s = 1/(1-2c)

1-2c = 1/s
c = 0.5-1/2s

s=2     -> c = 0.25
s=1.618 -> c = 0.1909765
s=1.5   -> c = 0.16666667
"""

import math
from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.color import lab


class Template:
    ENABLED: Final = "CTEnabled"
    GLOBAL_A: Final = "CTA1"
    GLOBAL_B: Final = "CTB1"
    SHADOW_A: Final = "CTA2"
    SHADOW_B: Final = "CTB2"
    MIDTONE_A: Final = "CTA3"
    MIDTONE_B: Final = "CTB3"
    HIGHLIGHT_A: Final = "CTA4"
    HIGHLIGHT_B: Final = "CTB4"


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    global_hcl = profile_params.colors.grading.toning.global_lch.as_list()
    shadow_hcl = profile_params.colors.grading.toning.shadow_lch.as_list()
    midtone_hcl = profile_params.colors.grading.toning.midtone_lch.as_list()
    highlight_hcl = profile_params.colors.grading.toning.highlight_lch.as_list()

    global_ab = lab.from_lch(global_hcl)[1:]
    shadow_ab = lab.from_lch(shadow_hcl)[1:]
    midtone_ab = lab.from_lch(midtone_hcl)[1:]
    highlight_ab = lab.from_lch(highlight_hcl)[1:]

    is_enabled = any(not math.isclose(x, 0) for x in
                     global_ab + shadow_ab + midtone_ab + highlight_ab)
    return {
        Template.ENABLED: str(is_enabled).lower(),
        Template.GLOBAL_A: str(global_ab[0] / 100),
        Template.GLOBAL_B: str(global_ab[1] / 100),
        Template.SHADOW_A: str(shadow_ab[0] / 100),
        Template.SHADOW_B: str(shadow_ab[1] / 100),
        Template.MIDTONE_A: str(midtone_ab[0] / 100),
        Template.MIDTONE_B: str(midtone_ab[1] / 100),
        Template.HIGHLIGHT_A: str(highlight_ab[0] / 100),
        Template.HIGHLIGHT_B: str(highlight_ab[1] / 100),
    }

