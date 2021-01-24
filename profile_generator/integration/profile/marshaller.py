from functools import partial

from profile_generator.feature import raw
from profile_generator.feature.details import noise_reduction
from profile_generator.feature.details.sharpening import capture, output
from profile_generator.feature.tone.contrast import bezier
from profile_generator.profile import marshaller

from .. import field_names

_TONE_CURVE_BEZIER = f"{field_names.TONE}.{field_names.CURVE}.{field_names.BEZIER}"
_NOISE_REDUCTION = f"{field_names.DETAILS}.{field_names.NOISE_REDUCTION}"
_CAPTURE_SHARPENING = (
    f"{field_names.DETAILS}.{field_names.SHARPENING}.{field_names.CAPTURE_SHARPENING}"
)
_OUTPUT_SHARPENING = (
    f"{field_names.DETAILS}.{field_names.SHARPENING}.{field_names.OUTPUT_SHARPENGING}"
)

marshallers = {
    field_names.RAW: raw.get_profile_args,
    _TONE_CURVE_BEZIER: bezier.get_profile_args,
    _NOISE_REDUCTION: noise_reduction.get_profile_args,
    _CAPTURE_SHARPENING: capture.get_profile_args,
    _OUTPUT_SHARPENING: output.get_profile_args,
}

get_profile_args = partial(marshaller.get_profile_args, **marshallers)
