"""Módulo de definição de constantes globais para o projeto."""

from pathlib import Path
from zoneinfo import ZoneInfo

APP_NAME: str = "portfolio-web-analytics"
"""Nome da aplicação: `portfolio-web-analytics`."""

VERSION: str = "0.1.0"
"""Versão da aplicação: `0.1.0`"""

SETTINGS_FILE: Path = Path("./src/config/files/settings.yaml")
"""Caminho para o arquivo de configuração global: `./src/config/files/settings.yaml`"""

PARSER_FILE: Path = Path("./src/config/files/parser.yaml")
"""Caminho para o arquivo de configuração do parser: `./src/config/files/parser.yaml`"""

DATASETS_DIR: Path = Path("./data/datasets")
"""Diretório para datasets: `./data/datasets`"""

HTML_DIR: Path = Path("./data/html")
"""Diretório para arquivos HTML: `./data/html`"""

OUTPUT_DIR: Path = Path("./data/output")
"""Diretório para resultados do pipeline: `./data/output`"""

BRT: ZoneInfo = ZoneInfo("America/Sao_Paulo")
"""Define o objeto de fuso horário para o horário de Brasília:  `America/Sao_Paulo`"""
