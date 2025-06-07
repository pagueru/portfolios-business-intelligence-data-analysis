from logging import Logger
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.common.echo import echo
from src.common.logger import LoggerSingleton
from src.core.errors import ProjectError
from src.pipeline.web_analytics_pipeline import WebAnalyticsPipeline
from src.repositories.config_repository import ConfigRepository
from src.repositories.goodreads_repository import GoodreadsRepository
from src.repositories.kaggle_repository import KaggleRepository
from src.repositories.parser_repository import ParserRepository

if __name__ == "__main__":
    try:
        logger: Logger = LoggerSingleton.logger or LoggerSingleton.get_logger()
        """Logger singleton para registrar eventos e erros."""

        # html_path = "./data/html/25986929-goodnight-punpun-omnibus-vol-1.html"
        """Caminho do arquivo HTML a ser carregado."""

        config_repository = ConfigRepository()
        """Inicia o repositório de configurações do projeto."""

        pipeline = WebAnalyticsPipeline(
            config_repository=config_repository,
            goodreads_repository=GoodreadsRepository(config_repository.goodreads_settings),
            kaggle_repository=KaggleRepository(config_repository.kaggle_settings),
            parser_repository=ParserRepository(),
        )
        """Inicia o pipeline de web analytics com os repositórios necessários."""

        # Executa o pipeline
        pipeline.run()
    except KeyboardInterrupt:
        logger.exception("Pipeline interrompida pelo usuário.")
        raise
    except FileNotFoundError:
        logger.exception("Arquivo não encontrado.")
        raise
    except RuntimeError:
        logger.exception("Erro de execução.")
        raise
    except ProjectError:
        logger.exception("Erro inesperado.")
        raise
