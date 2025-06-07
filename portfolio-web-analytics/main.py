from logging import Logger

from src.common.errors.errors import ProjectError
from src.config.settings_manager import SettingsManager
from src.infrastructure.datasources.goodreads_parser import GoodreadsParser
from src.infrastructure.datasources.goodreads_scraper import GoodreadsScraper
from src.infrastructure.datasources.kaggle_dataset_provider import KaggleDatasetProvider
from src.infrastructure.logger import LoggerSingleton
from src.pipeline.web_analytics_pipeline import WebAnalyticsPipeline

if __name__ == "__main__":
    try:
        logger: Logger = LoggerSingleton.logger or LoggerSingleton.get_logger()
        """Logger singleton para registrar eventos e erros."""

        config_repository = SettingsManager()
        """Inicia o repositório de configurações do projeto."""

        pipeline = WebAnalyticsPipeline(
            config_repository=config_repository,
            goodreads_repository=GoodreadsScraper(config_repository.goodreads_settings),
            kaggle_repository=KaggleDatasetProvider(config_repository.kaggle_settings),
            parser_repository=GoodreadsParser(),
        )
        """Inicia o pipeline de web analytics com os repositórios necessários."""

        # Executa o pipeline
        pipeline.run()
    except KeyboardInterrupt:
        logger.exception("Pipeline interrompida pelo usuário.")
        raise
    except ProjectError:
        logger.exception("Erro inesperado.")
        raise
