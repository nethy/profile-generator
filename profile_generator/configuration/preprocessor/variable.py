from abc import ABCMeta
from collections.abc import Mapping, MutableMapping, Sequence
from dataclasses import dataclass
from typing import Any


class VariableError(Exception, metaclass=ABCMeta):
    pass


@dataclass
class UndefinedVariableError(VariableError):
    variable_name: str


@dataclass
class IllegalReferenceError(VariableError):
    variable_name: str


def replace(
    data: MutableMapping[str, Any]
) -> tuple[Mapping[str, Any], Sequence[VariableError]]:
    result = data
    variables = result.pop("variables", {})
    return _replace(variables, result, "")


def _replace(
    variables: Mapping[str, Any], data: Any, context: str
) -> tuple[Any, Sequence[VariableError]]:
    if isinstance(data, str) and data.startswith("$"):
        if data[1:] in variables:
            return (variables[data[1:]], [])
        else:
            return (
                {},
                [UndefinedVariableError(_concat(context, data))],
            )
    elif isinstance(data, dict):
        return _replace_dict(variables, data, context)
    elif isinstance(data, list):
        return _replace_list(variables, data, context)
    else:
        return (data, [])


def _replace_dict(
    variables: Mapping[str, Any], data: Mapping[str, Any], context: str
) -> tuple[Mapping[str, Any], Sequence[VariableError]]:
    result: dict[str, Any] = {}
    errors: list[VariableError] = []
    for key, value in data.items():
        if key.startswith("$"):
            errors.append(IllegalReferenceError(_concat(context, key)))
        partial_result, partial_errors = _replace(
            variables, value, _concat(context, key)
        )
        result[key] = partial_result
        errors += partial_errors
    if len(errors) > 0:
        result.clear()
    return (result, errors)


def _replace_list(
    variables: Mapping[str, Any], data: Sequence[Any], context: str
) -> tuple[Sequence[Any], Sequence[VariableError]]:
    result: list[Any] = []
    errors: list[VariableError] = []
    for i, value in enumerate(data):
        partial_result, partial_errors = _replace(variables, value, f"{context}[{i}]")
        result.append(partial_result)
        errors += partial_errors
    if len(errors) > 0:
        result.clear()
    return (result, errors)


def _concat(left: str, right: str) -> str:
    if len(left) > 0:
        return left + "." + right
    else:
        return right
