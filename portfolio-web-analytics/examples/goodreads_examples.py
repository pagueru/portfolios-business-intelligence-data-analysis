from pathlib import Path
import sys

import python_path

from src.core.errors import ProjectError
from src.repositories.config_repository import ConfigRepository
from src.repositories.goodreads_repository import GoodreadsRepository

# Configuração necessária para inicializar a classe
manual_config = {
    "book_title": "PunPun",
    "book_url_base": "https://www.goodreads.com/book/show/",
    "book_fallback": "25986929-goodnight-punpun-omnibus-vol-1",
    "cache_seconds": 600,
    "html_output_directory": "./data/html/",
    "search_url_base": "https://www.goodreads.com/search?query=",
}

# Adicionando a classe de configuração do projeto
config_repository = ConfigRepository()

# Instanciando a classe
# repository = GoodreadsRepository(manual_config)
repository = GoodreadsRepository(config_repository.goodreads_settings)

# Chamando o método principal para realizar o download
try:
    html_path = repository.execute_download()
except ProjectError as e:
    print(f"Erro ao executar o download: {e}")
