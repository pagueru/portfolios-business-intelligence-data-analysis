"""Interface para o logger."""

from abc import ABC, abstractmethod


class ILogger(ABC):
    """Interface para o logger."""

    @abstractmethod
    def info(self, message: str) -> None:
        """Registra uma mensagem de informação."""

    @abstractmethod
    def warning(self, message: str) -> None:
        """Registra uma mensagem de aviso."""

    @abstractmethod
    def error(self, message: str) -> None:
        """Registra uma mensagem de erro."""

    @abstractmethod
    def debug(self, message: str) -> None:
        """Registra uma mensagem de depuração."""

    @abstractmethod
    def exception(self, message: str) -> None:
        """Registra uma mensagem exception."""

    @abstractmethod
    def critical(self, message: str) -> None:
        """Registra uma mensagem critical."""
