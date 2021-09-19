from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, range_of

_LC_ENABLED = "LCEnabled"
_LC_AMOUNT = "LCAmount"

_DEFAULT_LOCAL_CONTRAST = 0


def _process(data: Any) -> Mapping[str, str]:
    value = data.get("local", _DEFAULT_LOCAL_CONTRAST)
    amount = 0.05 * value
    enabled = str(value > _DEFAULT_LOCAL_CONTRAST).lower()
    return {_LC_ENABLED: enabled, _LC_AMOUNT: str(round(amount, 2))}


SCHEMA = object_of({"local": range_of(0, 10)}, _process)
