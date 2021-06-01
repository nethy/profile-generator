from collections.abc import Mapping
from typing import Any

from profile_generator.schema import object_of, type_of


def _process(data: Any) -> Mapping[str, str]:
    enabled = data.get("enabled", False)
    return {"PostDemosaicSharpeningEnabled": str(enabled).lower()}


SCHEMA = object_of({"enabled": type_of(bool)}, _process)
