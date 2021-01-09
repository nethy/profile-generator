from functools import partial
from profile import marshaller

from feature.tone import contrast

from .. import field_names

marshallers = {
    ".".join(
        [field_names.TONE, field_names.CURVE, field_names.BEZIER]
    ): contrast.bezier.get_profile_args
}

get_profile_args = partial(marshaller.get_profile_args, **marshallers)
