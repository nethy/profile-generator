from collections.abc import Callable, Mapping
from typing import Any

Marshaller = Callable[[Mapping[str, Any]], Mapping[str, str]]


def get_profile_args(
    configuration: Mapping[str, Any], **marshallers: Marshaller
) -> Mapping[str, str]:
    result: dict[str, str] = {}
    for key, marshaller in marshallers.items():
        configuration_part = _find_coniguration_part(key, configuration)
        result = {**result, **marshaller(configuration_part)}
    return result


def _find_coniguration_part(
    key: str, configuration: Mapping[str, Any]
) -> Mapping[str, Any]:
    configuration_part = configuration
    for key_part in key.split("."):
        configuration_part = configuration_part.get(key_part, {})
    return configuration_part
