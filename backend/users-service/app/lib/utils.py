from typing import Any

from pydantic import BaseModel


def validate_default_pydantic_fields(
    *, _class: BaseModel, data: dict[str, Any] | BaseModel
) -> set[str]:
    """function for validating if the fields in pydantic.BaseModel instance have default values"""
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


def validate_default_dataclass_fields(
    *, _class: Any, data: dict[str, Any] | Any
) -> set[str]:
    """function for validating if the fields in dataclasses.dataclass instance have default values"""
