from profile_generator.main.profile_params import DemosaicMethod
from profile_generator.schema import object_of, options_of, range_of, type_of

_ALGORITHM = "algorithm"
_AUTO_THRESHOLD = "auto_threshold"
_THRESHOLD = "threshold"


SCHEMA = object_of(
    {
        _ALGORITHM: options_of(
            DemosaicMethod.AMAZE.name,
            DemosaicMethod.AMAZE_BILINEAR.name,
            DemosaicMethod.AMAZE_VNG4.name,
            DemosaicMethod.DCB_BILINEAR.name,
            DemosaicMethod.DCB_VNG4.name,
            DemosaicMethod.LMMSE.name,
            DemosaicMethod.RCD_BILINEAR.name,
            DemosaicMethod.RCD_VNG4.name,
        ),
        _THRESHOLD: range_of(0, 100),
        _AUTO_THRESHOLD: type_of(bool),
    }
)
