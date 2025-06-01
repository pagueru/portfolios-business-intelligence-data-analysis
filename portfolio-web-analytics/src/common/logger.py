"""Módulo de Logger."""

import json
import logging
from pathlib import Path
import shutil
from typing import Any, ClassVar, Optional
import warnings

import yaml

from src.common.echo import echo
from src.config.constants import SETTINGS_FILE
from src.config.constypes import LoggerDict, PathLike
from src.core.base_class import BaseClass
from src.core.errors import LoggerError


class LoggerSingleton(BaseClass):
    """Singleton para gerenciamento centralizado de logging."""

    _instance: ClassVar[Optional["LoggerSingleton"]] = None  # Singleton: instância única da classe
    _initialized: bool = False  # Indica se o logger foi inicializado
    logger: logging.Logger | None = None  # Objeto Logger para registrar logs

    def __new__(cls, config: dict[str, Any] | None = None) -> "LoggerSingleton":  # noqa: ARG004
        """Cria ou retorna a instância única da classe Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Inicializa a instância do logger se ainda não estiver inicializada."""
        if self._initialized:
            return

        # Usa o config fornecido ou tenta carregar do arquivo
        if config is None:
            config = self.load_config_from_yaml(SETTINGS_FILE)
            if config is None:
                config = self.get_default_config()

        self._assign_config(config)  # Atribua configurações do dicionário à instância
        logger_instance = self._define_handlers()  # Crie e configure o logger com handlers
        self._logger = logger_instance  # Armazene o logger como atributo privado
        self.logger = logger_instance  # Garanta que o atributo público logger seja preenchido
        LoggerSingleton.logger = logger_instance  # Compartilhe o logger no singleton
        self._initialized = True  # Marque a instância como inicializada

    def _ensure_initialized(self) -> None:
        """Garante que o logger está inicializado."""
        if not self._initialized:
            self.__class__()  # Cria nova instância que será retornada pelo singleton

    def load_config_from_yaml(self, file_path: PathLike) -> LoggerDict | None:
        """Carrega a configuração do logger a partir de um arquivo YAML."""
        file_path = super()._ensure_path(file_path)
        if not file_path.is_file():
            echo(f"O arquivo de configuração {file_path} não foi encontrado.", "warn")
            return None
        try:
            echo(f"Carregando configuração de {file_path}...", "info")
            with file_path.open("r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
            echo("Configuração carregada com sucesso.", "success")
            super()._separator_line()
        except LoggerError as exc:
            echo(f"Erro ao carregar arquivo YAML: {exc}", "error")
            return None
        else:
            return config

    def get_default_config(self) -> LoggerDict:
        """Retorna a configuração padrão do logger."""
        return {
            "logger": {
                "file": {
                    "enabled": True,
                    "level": "DEBUG",
                    "path": "logs/app.log",
                },
                "console": {
                    "level": "INFO",
                },
            }
        }

    def _assign_config(self, config: LoggerDict) -> None:
        """Atribui as configurações do dicionário às variáveis da classe."""
        try:
            self.file_enabled: bool = bool(config["logger"]["file"]["enabled"])
            self.file_level: str = str(config["logger"]["file"]["level"])
            self.file_path: PathLike = str(config["logger"]["file"]["path"])
            self.console_level: str = str(config["logger"]["console"]["level"])
            self.suppress_list: list[str] = [
                str(item) for item in config["logger"].get("suppress", [])
            ]
            self.ignore_libs: list[str] = [
                str(lib) for lib in config["logger"].get("ignore_libs", [])
            ]
        except KeyError as exc:
            echo(f"Erro ao atribuir as chaves do dicionário de configurações: {exc}", "error")
            raise

    def _suppress_warnings(self) -> None:
        """Suprime warnings específicos e mensagens de bibliotecas configuradas."""
        # Suprime mensagens específicas
        try:
            if self.suppress_list:
                for warning_message in self.suppress_list:
                    warnings.filterwarnings(action="ignore", message=warning_message)
        except LoggerError:
            msg = "Erro ao suprimir warnings. Verifique a lista de mensagens."
            echo(msg, "error")
            raise

        # Ignora mensagens de bibliotecas específicas
        try:
            if hasattr(self, "ignore_libs") and self.ignore_libs:
                for lib in self.ignore_libs:
                    logging.getLogger(lib).setLevel(logging.CRITICAL)
        except LoggerError:
            msg = "Erro ao ignorar mensagens de bibliotecas. Verifique a lista de bibliotecas."
            echo(msg, "error")
            raise

    def _define_handlers(self) -> logging.Logger:
        """Configura e retorna um logger com handlers para console e arquivo (opcional)."""
        # Configura o root logger
        logging.basicConfig(level=logging.NOTSET)
        root_logger = logging.getLogger()

        # Remove handlers existentes para evitar duplicação
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Define o nível do logger
        root_logger.setLevel(getattr(logging, self.console_level, logging.INFO))

        # Configura o formato padrão
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(module)s:%(lineno)03d - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler de console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self.console_level, logging.INFO))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # Handler de arquivo (opcional)
        if self.file_enabled and self.file_path:
            try:
                file_path = super()._ensure_path(self.file_path)
                file_handler = logging.FileHandler(file_path, encoding="utf-8")
                file_handler.setLevel(getattr(logging, self.file_level, logging.DEBUG))
                file_handler.setFormatter(formatter)
                root_logger.addHandler(file_handler)
            except OSError:
                console_handler.setLevel(logging.ERROR)
                root_logger.exception("Erro ao configurar log de arquivo")

        self._suppress_warnings()

        return root_logger

    def dump_config(self) -> str:
        """Retorna a configuração da classe em um JSON dump sem identação."""
        return json.dumps(
            {
                "file_enabled": self.file_enabled,
                "file_level": self.file_level,
                "file_path": str(self.file_path),
                "console_level": self.console_level,
                "suppress_list": self.suppress_list,
            }
        )

    def info(self, message: str) -> None:
        """Loga uma mensagem de nível INFO."""
        if not self._initialized:
            self._ensure_initialized()
        self._logger.info(
            message, stacklevel=2
        )  # Usa stacklevel=2 para capturar o chamador correto

    def warning(self, message: str) -> None:
        """Loga uma mensagem de nível WARNING."""
        if not self._initialized:
            self._ensure_initialized()
        self._logger.warning(message, stacklevel=2)

    def error(self, message: str) -> None:
        """Loga uma mensagem de nível ERROR."""
        if not self._initialized:
            self._ensure_initialized()
        self._logger.error(message, stacklevel=2)

    def debug(self, message: str) -> None:
        """Loga uma mensagem de nível DEBUG."""
        if not self._initialized:
            self._ensure_initialized()
        self._logger.debug(message, stacklevel=2)

    def exception(self, message: str) -> None:
        """Loga uma mensagem de nível EXCEPTION."""
        if not self._initialized:
            self._ensure_initialized()
        self._logger.exception(message, stacklevel=2)

    def critical(self, message: str) -> None:
        """Loga uma mensagem de nível CRITICAL."""
        if not self._initialized:
            self._ensure_initialized()
        self._logger.critical(message, stacklevel=2)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Instancia o logger, inicializando-a  com a configuração padrão se necessário."""
        try:
            if cls._instance is None or cls._instance.logger is None:
                instance = cls()
                if instance.logger is None:
                    raise RuntimeError
                return instance.logger
        except LoggerError as exc:
            echo(f"Erro um erro ao instanciar o logger: {exc}", "error")
            raise
        else:
            return cls._instance.logger
