from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, options_of, range_of, type_of

_ALGORITHMS = {
    "amaze": "amaze",
    "amaze+vng4": "amazevng4",
    "dcb+vng4": "dcbvng4",
    "rcd+vng4": "rcdvng4",
    "lmmse": "lmmse",
}


_ALGORITHM = "algorithm"
_DEFAULT_ALGORITHM = _ALGORITHMS["amaze"]
_AUTO_THRESHOLD = "auto_threshold"
_DEFAULT_AUTO_THRESHOLD = True
_THRESHOLD = "threshold"
_DEFAULT_THRESHOLD = 20


def process(data: Any) -> Mapping[str, str]:
    algorithm = data.get(_ALGORITHM, _DEFAULT_ALGORITHM)
    auto_threshold = data.get(_AUTO_THRESHOLD, _DEFAULT_AUTO_THRESHOLD)
    threshold = data.get(_THRESHOLD, _DEFAULT_THRESHOLD)
    return {
        "BayerMethod": _ALGORITHMS.get(algorithm.lower(), _DEFAULT_ALGORITHM),
        "BayerDDAutoContrast": str(auto_threshold).lower(),
        "BayerDDContrast": str(threshold),
    }


SCHEMA = object_of(
    {
        _ALGORITHM: options_of("AMaZE", "AMaZE+VNG4", "DCB+VNG4", "RCD+VNG4", "LMMSE"),
        _THRESHOLD: range_of(0, 100),
        _AUTO_THRESHOLD: type_of(bool),
    }
)
