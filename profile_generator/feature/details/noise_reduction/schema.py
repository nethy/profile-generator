from profile_generator.main.profile_params import NoiseReductionMode
from profile_generator.schema import object_of, options_of, range_of

SCHEMA = object_of(
    {
        "mode": options_of(
            NoiseReductionMode.CONSERVATIVE.name, NoiseReductionMode.AGGRESSIVE.name
        ),
        "luminance": range_of(0, 100),
        "detail": range_of(0, 100),
        "chrominance": range_of(0, 100),
    }
)
