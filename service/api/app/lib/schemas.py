from typing import Any

import msgspec
from pydantic import BaseModel, ConfigDict


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


class PydanticBaseModel(BaseModel):
    """"""

    model_config = ConfigDict(
        validate_assignment=True,
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )
