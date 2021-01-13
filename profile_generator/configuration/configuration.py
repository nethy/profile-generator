from functools import reduce
from typing import Any, Callable, Dict

Configuration = Dict[str, Dict[str, Any]]


def create_from_template(
    template: Dict[str, Any], preprocess: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> Configuration:
    defaults = template.get("defaults", {})
    templates = template.get("templates", [])

    defaults = preprocess(defaults)
    templates = [
        {key: preprocess(value) for key, value in template.items()}
        for template in templates
    ]

    if len(templates) == 0:
        return {"Default": defaults}

    first_template, *rest_templates = templates
    first_cfg = _merge_first_template(defaults, first_template)
    return reduce(_merge_template, rest_templates, first_cfg)


def _merge_first_template(
    defaults: Dict[str, Any], template: Configuration
) -> Configuration:
    return {name: _merge_dicts(defaults, body) for name, body in template.items()}


def _merge_template(
    configuration: Configuration, template: Configuration
) -> Configuration:
    return {
        cfg_name + "_" + template_name: _merge_dicts(cfg_body, template_body)
        for cfg_name, cfg_body in configuration.items()
        for template_name, template_body in template.items()
    }


def _merge_dicts(base: Dict[str, Any], overrider: Dict[str, Any]) -> Dict[str, Any]:
    merged = base.copy()
    for key, value in overrider.items():
        if isinstance(value, dict):
            default_value = merged.get(key, {})
            merged[key] = _merge_dicts(default_value, value)
        else:
            merged[key] = value
    return merged
