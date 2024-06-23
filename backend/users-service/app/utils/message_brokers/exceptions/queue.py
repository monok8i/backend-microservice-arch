from dataclasses import dataclass

from .base import BaseBrokerException

@dataclass(eq=False)
class QueueNotFoundException(BaseBrokerException):
    ...