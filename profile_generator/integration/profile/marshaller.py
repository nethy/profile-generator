from functools import partial
from profile import marshaller

from feature import raw
from feature.tone.contrast import bezier

from .. import field_names

marshallers = {
    ".".join(
        [field_names.TONE, field_names.CURVE, field_names.BEZIER]
    ): bezier.get_profile_args,
    field_names.RAW: raw.get_profile_args,
}

get_profile_args = partial(marshaller.get_profile_args, **marshallers)
