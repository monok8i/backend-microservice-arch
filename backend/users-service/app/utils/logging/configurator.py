import logging
from dataclasses import dataclass
from typing import TypeVar

from .handlers.base import BaseLoggingHandler

CustomHandler = TypeVar("CustomHandler", bound=BaseLoggingHandler)


@dataclass
class Logger:
    name: str
    level: int
    propagate: bool
    handlers: list[CustomHandler]

    def configure(self) -> None:
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.propagate = self.propagate
        logger.handlers = [handler for handler in self.handlers]


@dataclass
class LoggersConfigurator:
    loggers: list[Logger] = None

    def add_logger(self, logger: Logger) -> None:
        self.loggers.append(logger)

    def configure_loggers(self) -> logging.Logger: 
        for logger in self.loggers:
            logger.configure()

    
