# from typing import Any

# from dataclasses import fields, dataclass, _MISSING_TYPE, is_dataclass, asdict
# from pydantic import BaseModel


# def validate_default_pydantic_fields(
#     *, _class: BaseModel, data: dict[str, Any] | BaseModel
# ) -> set[str]:
#     """function for validating if the fields in pydantic.BaseModel instance have default values"""
#     defaults = set()
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if hasattr(_class, key):
#                 if value == _class.model_fields.get(key).default:
#                     defaults.add(key)
#         return defaults
#     for key, value in data.model_dump().items():
#         if hasattr(_class, key):
#             if value == _class.model_fields.get(key).default:
#                 defaults.add(key)
#     return defaults


# def validate_default_dataclass_fields(
#     *, _class: Any, data: dict[str, Any] | Any = None
# ) -> set[str]:
#     """function for validating if the fields in dataclasses.dataclass instance have default values"""
#     defaults = set()
#     # if isinstance(data, dict):
#     #     for key, value in data.items():
#     #         if hasattr(_class, key):
#     #             if value == _class.__dataclass_fields__[key].default:
#     #                 defaults.add(key)

#     # alternative
#     _fields = {f.name: f.default for f in fields(_class) if not isinstance(f.default, _MISSING_TYPE)}
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if hasattr(_class, key):
#                 if value == _fields.get(key):
#                     defaults.add(key)
#     if is_dataclass(data):
#         for key, value in asdict(data).items():
#             if hasattr(_class, key):
#                 if value == _fields.get(key):
#                     defaults.add(key)
#     return defaults
    
