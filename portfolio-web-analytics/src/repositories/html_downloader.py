"""Classe para baixar HTML de páginas e salvar localmente."""

import datetime
from pathlib import Path

import httpx

from src.common.logger import LoggerSingleton
from src.config.constants import CACHE_SECONDS, DATA_DIR, GOODREADS_BOOK_URL
from src.core.base_class import BaseClass
from src.core.errors import HTMLDownloaderError


class HTMLDownloader(BaseClass):
    """Baixa o HTML de uma página e salva em disco."""

    def __init__(self, url: str, output_dir: Path | None) -> None:
        """Inicializa as instâncias."""
        self.url = url
        self.prefix = GOODREADS_BOOK_URL
        self.cache_seconds = CACHE_SECONDS
        self.cache_minutes = CACHE_SECONDS // 60
        self.output_dir = self._output_path(output_dir)
        self.logger = LoggerSingleton().logger or LoggerSingleton.get_logger()
        self.class_name = self.__class__.__name__

    def _output_path(self, output_dir: Path | None) -> Path:
        """Verifica se a pasta existe, se não, atribui './data' e cria."""
        if not output_dir:
            output_dir = Path(DATA_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def get_filename_from_url(self) -> str:
        """Extrai o nome do arquivo a partir da URL do Goodreads."""
        if self.url.startswith(self.prefix):
            return self.url[len(self.prefix) :].rstrip("/") + ".html"
        return self.url.rstrip("/").split("/")[-1] + ".html"

    def is_file_cache_valid(self, file_path: Path) -> bool:
        """Verifica se o arquivo existe e ainda está dentro do período de cache válido."""
        if not file_path.exists():
            self.logger.error(f"Arquivo não encontrado: {file_path}")
            return False

        mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime, tz=datetime.UTC)
        now = datetime.datetime.now(tz=datetime.UTC)
        return (now - mtime).total_seconds() < self.cache_seconds

    def get_or_download_html(self) -> Path:
        """Baixa e salva o HTML usando o nome extraído da URL como nome do arquivo."""
        try:
            filename = self.get_filename_from_url()
            output_path = self.output_dir / filename

            if output_path.exists():
                self.logger.debug(f"Arquivo HTML identificado: '{output_path.name}'")

            if self.is_file_cache_valid(output_path):
                self.logger.debug(f"Arquivo modificado há menos de {self.cache_minutes} minutos.")
                return output_path

            return self.download_html(filename=filename)
        except HTMLDownloaderError:
            self.logger.exception(f"Erro ao verificar cache ou baixar HTML de '{self.url}'.")
            raise

    def download_html(self, filename: str | None = None) -> Path:
        """Baixa o HTML e salva no arquivo especificado."""
        output_path = None  # Inicializa a variável para evitar erros no bloco except
        try:
            self.logger.debug(f"Baixando HTML de: '{self.url}'")
            with httpx.Client(timeout=20.0, follow_redirects=True) as client:
                response = client.get(self.url)
                response.raise_for_status()
                html = response.text
        except httpx.HTTPStatusError:
            self.logger.exception(f"Erro ao baixar o HTML de '{self.url}'")
            raise
        try:
            if not filename:
                filename = self.url.rstrip("/").split("/")[-1] + ".html"

            output_path = self.output_dir / filename
            output_path.write_text(html, encoding="utf-8")

        except OSError:
            if output_path is None:
                self.logger.exception("Erro ao salvar o HTML, caminho não definido.")
            self.logger.exception(f"Erro ao salvar o HTML em '{output_path}'")
            raise

        except HTMLDownloaderError:
            self.logger.exception(self._raise_error())
            raise
        else:
            self.logger.debug(f"HTML salvo em '{output_path}'")
            return output_path
