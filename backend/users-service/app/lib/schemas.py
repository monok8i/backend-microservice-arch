import msgspec
from typing import Any, Tuple, List, Self, Set, Dict

from dataclasses import dataclass, asdict, is_dataclass

from pydantic import BaseModel


@dataclass
class DataclassDictModel:
    """Base class for dataclass objects"""

    def to_dict(
        cls,
        exclude: List[str] | Tuple[str] | Set[str] = None,
        with_values: bool = False,
    ) -> Dict[str, Any] | Tuple[Dict[str, Any], int]:
        if exclude:
            if with_values:
                data = asdict(cls)
                excluded = []
                for key in exclude:
                    if key in data.keys():
                        excluded.append(data.pop(key, None))
                return data, excluded
            data = asdict(cls)
            for key in exclude:
                if key in data.keys():
                    del data[key]
            return data
        return asdict(cls)

    def from_dict(cls, data: dict) -> Self:
        if is_dataclass(cls):
            for key in data.keys():
                if hasattr(cls, key):
                    setattr(cls, key, data[key])
            return cls
        raise TypeError("from_dict() should be callad on dataclass instances")


class BaseStructModel(msgspec.Struct):
    def to_dict(self) -> dict[str, Any]:
        return {
            f: getattr(self, f)
            for f in self.__struct_fields__
            if getattr(self, f, None) != msgspec.UNSET
        }


class CamelizedBaseStructModel(BaseStructModel, rename="camel"):
    """Camelized Base Struct class for custom data objects"""


class Message(CamelizedBaseStructModel):
    message: str


class PydanticDefaultsModel(BaseModel):
    """"""

    def validate_into_defaults(cls, data: dict[str, Any] | BaseModel) -> set[str]:
        defaults = set()
        if isinstance(data, dict):
            for key, value in data.items():
                if hasattr(cls, key):
                    if value == cls.model_fields[key].default:
                        defaults.add(key)
            return defaults
        for key, value in data.model_dump().items():
            if hasattr(cls, key):
                if value == cls.model_fields[key].default:
                    defaults.add(key)
        return defaults
