from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams

from .demosaic.profile_generator import generate as generate_demosaic


class Template:
    RED: Final = "BayerPreBlackRed"
    GREEN: Final = "BayerPreBlackGreen"
    BLUE: Final = "BayerPreBlackBlue"


def generate(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    return {
        **_get_raw(profile_params, exclude_default),
        **generate_demosaic(profile_params, exclude_default),
    }


def _get_raw(profile_params: ProfileParams, exclude_default: bool) -> Mapping[str, str]:
    black_points = profile_params.raw.black_points
    if exclude_default and not black_points.is_set:
        return {}

    return {
        name: str(value)
        for name, value in zip(
            (
                Template.RED,
                Template.GREEN,
                Template.BLUE,
            ),
            profile_params.raw.black_points.value,
        )
    }
