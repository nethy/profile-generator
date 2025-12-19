from collections.abc import Mapping
from typing import Any


def get_fields(clazz: Any) -> Mapping[str, Any]:
    return {
        name: value
        for name, value in clazz.__dict__.items()
        if not name.startswith("__")
    }
