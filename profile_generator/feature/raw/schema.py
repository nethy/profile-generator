from collections.abc import Mapping
from typing import Any, Final

from profile_generator.schema import composite_process, object_of, range_of, tuple_of

from . import demosaic

_DEMOSAIC_FIELD = "demosaic"


class _BlackPoint:
    FIELD: Final = "black_points"
    RANGE: Final = range_of(-2048, 2048)
    DEFAULT: Final = [0, 0, 0]
    RED_TEMPLATE: Final = "BayerPreBlackRed"
    GREEN_TEMPLATE: Final = "BayerPreBlackGreen"
    BLUE_TEMPLATE: Final = "BayerPreBlackBlue"


def _process(data: Any) -> Mapping[str, str]:
    black_points = data.get(_BlackPoint.FIELD, _BlackPoint.DEFAULT)
    return {
        name: str(value)
        for name, value in zip(
            (
                _BlackPoint.RED_TEMPLATE,
                _BlackPoint.GREEN_TEMPLATE,
                _BlackPoint.BLUE_TEMPLATE,
            ),
            black_points,
        )
    }


SCHEMA = object_of(
    {
        _DEMOSAIC_FIELD: demosaic.SCHEMA,
        _BlackPoint.FIELD: tuple_of(
            _BlackPoint.RANGE, _BlackPoint.RANGE, _BlackPoint.RANGE
        ),
    },
    composite_process(_process, {_DEMOSAIC_FIELD: demosaic.process}),
)
