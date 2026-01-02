from collections.abc import Mapping, Sequence, Set


def get_sections(profile_template: str) -> Mapping[str, Sequence[str]]:
    parameters_by_section: dict[str, list[str]] = {}
    section_name = None
    section_params: list[str] = []
    for line in profile_template.splitlines():
        if len(line) == 0:
            continue
        if line[-1] == "]":
            _add_section(parameters_by_section, section_name, section_params)
            section_name = line[1:-1]
            section_params = []
        elif line[-1] == "}":
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


def get_partial_template(
    sections: Mapping[str, Sequence[str]], parameters: Set[str]
) -> str:
    relevant_sections = _filter_sections_by_parameters(sections, parameters)
    return _to_str(relevant_sections)


def _filter_sections_by_parameters(
    sections: Mapping[str, Sequence[str]], params: Set[str]
) -> dict[str, list[str]]:
    relevant_sections: dict[str, list[str]] = {}
    remaining_params = list(params)
    for section_name, section_params in sections.items():
        for section_param in section_params:
            _filter_section_by_parameters(
                relevant_sections, remaining_params, section_name, section_param
            )
    return relevant_sections


def _filter_section_by_parameters(
    relevant_sections: dict[str, list[str]],
    remaining_params: list[str],
    section_name: str,
    section_param: str,
) -> None:
    param_index = _find_param_index(section_param, remaining_params)
    if param_index is not None:
        if relevant_sections.get(section_name) is None:
            relevant_sections[section_name] = []
        relevant_sections[section_name].append(section_param)
        remaining_params.pop(param_index)


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
