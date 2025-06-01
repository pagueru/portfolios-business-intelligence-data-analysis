"""Módulo de definição de constantes globais para o projeto."""

from zoneinfo import ZoneInfo

from src.config.constypes import PathLike

APP_NAME: str = "portfolio-web-analytics"
"""Nome da aplicação: `portfolio-web-analytics`."""

VERSION: str = "0.1.0"
"""Versão da aplicação: `0.1.0`"""

SETTINGS_FILE: PathLike = "./src/config/settings.yaml"
"""Caminho para o arquivo de configuração global: `./src/config/settings.yaml`"""

DATASETS_DIR: PathLike = "./data/datasets"
"""Diretório para datasets: `./data/datasets`"""

DATA_DIR: PathLike = "./data"
"""Diretório para dados: `./data`"""

BRT: ZoneInfo = ZoneInfo("America/Sao_Paulo")
"""Define o objeto de fuso horário para o horário de Brasília:  `America/Sao_Paulo`"""

CACHE_SECONDS: int = 600
"""Número de segundos para considerar um arquivo como cache: `10 minutos`"""

GOODREADS_BOOK_URL: str = "https://www.goodreads.com/book/show/"
"""URL base do Goodreads para livros: `https://www.goodreads.com/book/show/`"""

GOODREADS_SEARCH_URL: str = "https://www.goodreads.com/search?query="
"""URL base do Goodreads para buscas de livros: `https://www.goodreads.com/search?query=`"""
