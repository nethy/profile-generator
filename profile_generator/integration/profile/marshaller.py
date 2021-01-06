from functools import partial
from profile import marshaller

from feature.tone import contrast_bezier

from .. import field_names


def _tone(field: str) -> str:
    return field_names.TONE + "." + field


marshallers = {_tone(field_names.CONTRAST_BEZIER): contrast_bezier.get_profile_args}

get_profile_args = partial(marshaller.get_profile_args, **marshallers)
