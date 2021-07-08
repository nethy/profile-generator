from collections.abc import Callable, Mapping
from typing import Any

Processor = Callable[[Any], Mapping[str, str]]


def composite_process(
    local_process: Processor, processes: Mapping[str, Processor]
) -> Callable[[Any], Mapping[str, str]]:
    def _processor(data: Any) -> Mapping[str, str]:
        local_data = {key: data[key] for key in data if key not in processes}
        result = dict(local_process(local_data))
        partial_results = (
            process(data.get(field, {})) for field, process in processes.items()
        )
        result |= {
            key: value
            for partial_result in partial_results
            for key, value in partial_result.items()
        }
        return result

    return _processor
