from profile_generator.main.profile_params import DemosaicMethod
from profile_generator.schema import object_of, options_of, range_of, type_of

SCHEMA = object_of(
    {
        "algorithm": options_of(
            DemosaicMethod.AMAZE.name,
            DemosaicMethod.AMAZE_BILINEAR.name,
            DemosaicMethod.AMAZE_VNG4.name,
            DemosaicMethod.DCB_BILINEAR.name,
            DemosaicMethod.DCB_VNG4.name,
            DemosaicMethod.LMMSE.name,
            DemosaicMethod.RCD_BILINEAR.name,
            DemosaicMethod.RCD_VNG4.name,
        ),
        "threshold": range_of(0, 100),
        "auto_threshold": type_of(bool),
    }
)
