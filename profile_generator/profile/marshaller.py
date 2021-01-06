from typing import Any, Callable, Dict

Marshaller = Callable[[Dict[str, Any]], Dict[str, str]]


def get_profile_args(
    configuration: Dict[str, Any], **marshallers: Marshaller
) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for key, marshaller in marshallers.items():
        configuration_part = _find_coniguration_part(key, configuration)
        result = {**result, **marshaller(configuration_part)}
    return result


def _find_coniguration_part(key: str, configuration: Dict[str, Any]) -> Dict[str, Any]:
    configuration_part = configuration
    for key_part in key.split("."):
        configuration_part = configuration_part.get(key_part, {})
    return configuration_part
