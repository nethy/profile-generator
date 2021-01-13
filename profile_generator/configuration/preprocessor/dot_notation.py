from typing import Any, Dict


def expand(configuration: Dict[str, Any]) -> Dict[str, Any]:
    expanded: Dict[str, Any] = {}
    for key, value in configuration.items():
        expanded = _merge(expanded, _expand_item(key, value))
    return expanded


def _expand_item(key: str, value: Any) -> Dict[str, Any]:
    idx = key.find(".")
    if idx > 0:
        head, tail = key[:idx], key[idx + 1 :]
        return {head: _expand_item(tail, value)}
    else:
        if isinstance(value, dict):
            return {key: expand(value)}
        else:
            return {key: value}


def _merge(base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    result = base
    for key, value in update.items():
        if key in result:
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result
