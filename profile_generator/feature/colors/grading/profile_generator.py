from collections.abc import Mapping
from typing import Final

from profile_generator.main.profile_params import ProfileParams
from profile_generator.model.view import raw_therapee

from .bsh import generate as generate_bsh
from .matte import generate as generate_matte
from .toning import generate as generate_toning


def generate(profile_params: ProfileParams) -> Mapping[str, str]:
    return (generate_bsh(profile_params)
            | generate_toning(profile_params)
            | generate_matte(profile_params))

