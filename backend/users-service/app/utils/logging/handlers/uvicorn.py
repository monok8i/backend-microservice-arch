from dataclasses import dataclass

from .base import BaseLoggingHandler


@dataclass
class UvicornLoggingHandler(BaseLoggingHandler): ...
