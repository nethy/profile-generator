"""
S ST MT M

S = 0, M = 0.5
ST-S = 2(M-MT)
ST = 2(0.5-MT)
ST = 1-2MT

MT-ST = 0.25
MT = 0.25+ST

ST = 1-0.5-2ST
3ST = 0.5
ST = 0.5/3
MT = 0.25+0.5/3

"""

import math
from collections.abc import Mapping

from profile_generator.main.profile_params import ColorToningChannel, ProfileParams
from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import EqPoint
from profile_generator.unit import Vector


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    toning_params = profile_params.colors.grading.toning
    shadow, midtone, highlight = (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)
    shadow_mask, midtone_mask, highlight_mask = [], [], []
    if (
        toning_params.channels.is_set
        and toning_params.channels.value == ColorToningChannel.ONE
    ):
        midtone_lch = toning_params.midtone.as_list()
        midtone = _lch_to_ab(midtone_lch)
    elif (
        toning_params.channels.is_set
        and toning_params.channels.value == ColorToningChannel.TWO
    ):
        shadow_lch = toning_params.shadow.as_list()
        highlight_lch = toning_params.highlight.as_list()
        shadow = _lch_to_ab(shadow_lch)
        highlight = _lch_to_ab(highlight_lch)
        shadow_mask = [EqPoint(1 / 3, 1), EqPoint(2 / 3, 0)]
        highlight_mask = [EqPoint(1 / 3, 0), EqPoint(2 / 3, 1)]
    elif (
        toning_params.channels.is_set
        and toning_params.channels.value == ColorToningChannel.THREE
    ):
        shadow_lch = toning_params.shadow.as_list()
        midtone_lch = toning_params.midtone.as_list()
        highlight_lch = toning_params.highlight.as_list()
        shadow = _lch_to_ab(shadow_lch)
        midtone = _lch_to_ab(midtone_lch)
        highlight = _lch_to_ab(highlight_lch)
        shadow_mask = [EqPoint(0.5 / 3, 1), EqPoint(0.25 + 0.5 / 3, 0)]
        midtone_mask = [
            EqPoint(0.5 / 3, 0),
            EqPoint(0.25 + 0.5 / 3, 1),
            EqPoint(1 - 0.25 - 0.5 / 3, 1),
            EqPoint(1 - 0.5 / 3, 0),
        ]
        highlight_mask = [EqPoint(1 - 0.25 - 0.5 / 3, 0), EqPoint(1 - 0.5 / 3, 1)]

    is_enabled = not any(
        map(lambda color: math.isclose(color, 0), (*shadow, *midtone, *highlight))
    )
    return {
        "CTEnabled": str(is_enabled).lower(),
        "CTShadowA": str(shadow[0] / 100),
        "CTShadowB": str(shadow[1] / 100),
        "CTShadowMask": raw_therapee.present_equalizer(shadow_mask),
        "CTMidtoneA": str(midtone[0] / 100),
        "CTMidtoneB": str(midtone[1] / 100),
        "CTMidtoneMask": raw_therapee.present_equalizer(midtone_mask),
        "CTHighlightA": str(highlight[0] / 100),
        "CTHighlightB": str(highlight[1] / 100),
        "CTHighlightMask": raw_therapee.present_equalizer(highlight_mask),
    }


def _lch_to_ab(lch: Vector) -> tuple[float, float]:
    return (
        lch[1] * math.cos(math.radians(lch[2])),
        lch[1] * math.sin(math.radians(lch[2])),
    )
