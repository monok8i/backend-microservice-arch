from dataclasses import dataclass

from .base import BaseLoggingHandler


@dataclass
class SQLALchemyLoggingHandler(BaseLoggingHandler): ...
