from collections.abc import Set


def extract_partial(profile_template: str, parameters: Set[str]) -> str:
    sections = _get_sections_by_parameters(profile_template, parameters)
    return _to_str(sections)


def _get_sections_by_parameters(
    profile_template: str, params: Set[str]
) -> dict[str, list[str]]:
    parameters_by_section: dict[str, list[str]] = {}
    section_name = None
    section_params: list[str] = []
    remaining_params = list(params)
    for line in profile_template.splitlines():
        if len(line) > 0 and line[0] == "[":
            _add_section(parameters_by_section, section_name, section_params)
            section_name = line[1:-1]
            section_params = []
        elif "{" in line:
            idx = _find_param_index(line, remaining_params)
            if idx is not None:
                remaining_params.pop(idx)
                section_params.append(line)
    _add_section(parameters_by_section, section_name, section_params)
    return parameters_by_section


def _add_section(
    parameters_by_section: dict[str, list[str]],
    section: str | None,
    parameters: list[str],
) -> None:
    if section is not None and len(parameters) > 0:
        parameters_by_section[section] = parameters


def _find_param_index(line: str, params: list[str]) -> int | None:
    for i, param in enumerate(params):
        if param in line:
            return i
    return None


def _to_str(parameters_by_section: dict[str, list[str]]) -> str:
    result = ""
    for section, parameters in parameters_by_section.items():
        result += "[" + section + "]" + "\n"
        for parameter in parameters:
            result += parameter + "\n"
        result += "\n"
    if len(parameters_by_section) > 0:
        result = result[:-1]
    return result
