import pathfix  # noqa: F401

from src.common.errors.errors import ProjectError
from src.config.settings_manager import SettingsManager
from src.infrastructure.datasources.goodreads_scraper import GoodreadsScraper

try:
    # Adicionando a classe de configuração do projeto
    config_repository = SettingsManager()

    # Instanciando a classe
    repository = GoodreadsScraper(config_repository.goodreads_settings)

    # Chamando o método principal
    html_path = repository.execute_download()

except ProjectError as e:
    print(f"Erro ao executar o download: {e}")
