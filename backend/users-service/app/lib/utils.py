from typing import Any

from pydantic import BaseModel


def validate_default_pydantic_fields(
    *, _class: BaseModel, data: dict[str, Any] | BaseModel
) -> set[str]:
    defaults = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if hasattr(_class, key):
                if value == _class.model_fields[key].default:
                    defaults.add(key)
        return defaults
    for key, value in data.model_dump().items():
        if hasattr(_class, key):
            if value == _class.model_fields[key].default:
                defaults.add(key)
    return defaults
