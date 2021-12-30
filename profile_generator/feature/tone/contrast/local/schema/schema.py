from collections.abc import Mapping
from typing import Any

from profile_generator.model.view import raw_therapee
from profile_generator.model.view.raw_therapee import LinearEqPoint
from profile_generator.schema import object_of, range_of

_DPE_ENABLED = "DPEEnabled"
_DPE_MULT_2 = "DPEMult2"
_DPE_MULT_3 = "DPEMult3"
_DPE_MULT_4 = "DPEMult4"
_DPE_MULT_5 = "DPEMult5"

_DEFAULT_LOCAL_CONTRAST = 0


def _process(data: Any) -> Mapping[str, str]:
    value = data.get("local", _DEFAULT_LOCAL_CONTRAST)
    amount = 1 + 0.1 * value
    edge_amount = 1 + 0.05 * value
    enabled = str(value > _DEFAULT_LOCAL_CONTRAST).lower()
    return {
        _DPE_ENABLED: enabled,
        _DPE_MULT_2: str(edge_amount),
        _DPE_MULT_3: str(amount),
        _DPE_MULT_4: str(amount),
        _DPE_MULT_5: str(edge_amount),
    }


SCHEMA = object_of({"local": range_of(0, 10)}, _process)
