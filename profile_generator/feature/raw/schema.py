from profile_generator.schema import composite_process, object_of

from . import demosaic

_DEMOSAIC = "demosaic"

SCHEMA = object_of(
    {_DEMOSAIC: demosaic.SCHEMA},
    composite_process(lambda _: {}, {_DEMOSAIC: demosaic.process}),
)
