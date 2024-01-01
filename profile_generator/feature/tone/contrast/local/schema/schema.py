from collections.abc import Mapping
from typing import Any, Final

from profile_generator.schema import object_of, range_of


class Template:
    DPE_ENABLED: Final = "DPEEnabled"
    DPE_MULT_2: Final = "DPEMult2"
    DPE_MULT_3: Final = "DPEMult3"
    DPE_MULT_4: Final = "DPEMult4"
    DPE_MULT_5: Final = "DPEMult5"


class Field:
    LOCAL: Final = "local"


class Default:
    LOCAL_CONTRAST: Final = 0


def _process(data: Any) -> Mapping[str, str]:
    value = data.get(Field.LOCAL, Default.LOCAL_CONTRAST)
    primary = 1 + 0.1 * value
    secondary = 1 + 0.05 * value
    tertiary = 1 + 0.025 * value
    enabled = str(value > Default.LOCAL_CONTRAST).lower()
    return {
        Template.DPE_ENABLED: enabled,
        Template.DPE_MULT_2: str(secondary),
        Template.DPE_MULT_3: str(primary),
        Template.DPE_MULT_4: str(secondary),
        Template.DPE_MULT_5: str(tertiary),
    }


SCHEMA = object_of({Field.LOCAL: range_of(0.0, 10.0)}, _process)
