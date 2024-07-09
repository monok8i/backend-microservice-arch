from dataclasses import dataclass


@dataclass(eq=False)
class BaseBrokerException(Exception):
    text: str
