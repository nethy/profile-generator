import os
from collections.abc import Set


def extract_partial(profile_template: str, sections: Set[str]) -> str:
    parameters_by_section = _get_parameters_by_section(profile_template, sections)
    return _to_str(parameters_by_section)


def _get_parameters_by_section(
    profile_template: str, sections: Set[str]
) -> dict[str, list[str]]:
    parameters_by_section: dict[str, list[str]] = {}
    section = None
    parameters: list[str] = []
    for line in profile_template.splitlines():
        if len(line) > 0 and line[0] == "[":
            _add_section(parameters_by_section, section, parameters)
            section = line[1:-1].casefold()
            section = section if section in sections else None
            parameters = []
        elif section is not None and "{" in line:
            parameters.append(line)
    _add_section(parameters_by_section, section, parameters)
    return parameters_by_section


def _add_section(
    parameters_by_section: dict[str, list[str]],
    section: str | None,
    parameters: list[str],
) -> None:
    if section is not None and len(parameters) > 0:
        parameters_by_section[section] = parameters


def _to_str(parameters_by_section: dict[str, list[str]]) -> str:
    result = ""
    for section, parameters in parameters_by_section.items():
        result += "[" + section + "]" + os.linesep
        for parameter in parameters:
            result += parameter + os.linesep
        result += os.linesep
    return result
