from functools import partial
from profile import marshaller

from feature import raw
from feature.details.sharpening import capture
from feature.tone.contrast import bezier

from .. import field_names

marshallers = {
    field_names.RAW: raw.get_profile_args,
    ".".join(
        [field_names.TONE, field_names.CURVE, field_names.BEZIER]
    ): bezier.get_profile_args,
    ".".join(
        [field_names.DETAILS, field_names.SHARPENING, field_names.CAPTURE_SHARPENING]
    ): capture.get_profile_args,
}

get_profile_args = partial(marshaller.get_profile_args, **marshallers)
