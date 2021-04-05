from typing import Any


def expand(element: Any) -> Any:
    if isinstance(element, dict):
        expanded: dict[str, Any] = {}
        for key, value in element.items():
            expanded = _merge(expanded, _expand_item(key, value))
        return expanded
    elif isinstance(element, list):
        return [expand(item) for item in element]
    else:
        return element


def _expand_item(key: str, value: Any) -> dict[str, Any]:
    idx = key.find(".")
    if idx > 0:
        head, tail = key[:idx], key[idx + 1 :]
        return {head: _expand_item(tail, value)}
    else:
        return {key: expand(value)}


def _merge(base: dict[str, Any], update: dict[str, Any]) -> dict[str, Any]:
    result = base
    for key, value in update.items():
        if key in result:
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result
