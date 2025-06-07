"""Classe para baixar HTML de páginas e salvar localmente."""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from bs4 import BeautifulSoup
from bs4.element import Tag
import httpx

from src.common.base.base_class import BaseClass
from src.common.errors.errors import GoodreadsScraperError
from src.config.constants import BRT, HTML_DIR
from src.infrastructure.logger import LoggerSingleton

if TYPE_CHECKING:
    from logging import Logger


class GoodreadsScraper(BaseClass):
    """Baixa o HTML de uma página e salva em disco."""

    def __init__(self, goodreads_config: dict[str, Any]) -> None:
        self.logger: Logger = LoggerSingleton.logger or LoggerSingleton.get_logger()
        """Logger singleton para registrar eventos e erros."""

        # Registra a inicialização da classe
        self.logger.info(super()._inicialize_class())

        self.class_name: str = self.__class__.__name__
        """Nome da classe atual para uso em logs e mensagens de erro: `HTMLDownloader`"""

        self.search_book_title: str = goodreads_config["search_book_title"]
        """Título do livro a ser pesquisado no Goodreads. Ex.: `PunPun`"""

        self.goodreads_book_url_base: str = goodreads_config["book_url_base"]
        """URL base do livro no Goodreads. Ex.: `https://www.goodreads.com/book/show/`"""

        self.fallback_book_id: str = goodreads_config["book_fallback"]
        """ID de fallback para busca de livros. Ex.: `25986929-goodnight-punpun-omnibus-vol-1`"""

        self.cache_duration_seconds: int = goodreads_config["cache_seconds"]
        """Período de cache em segundos. Ex.: `600`"""

        self.output_html_directory: Path = HTML_DIR
        """Diretório onde os arquivos HTML serão salvos: `./data/html/`"""

        self.goodreads_search_url: str = (
            goodreads_config["search_url_base"] + self.search_book_title
        )
        """URL de pesquisa no Goodreads: `https://www.goodreads.com/search?q={book_title}`"""

        self.fallback_book_url: str = self.goodreads_book_url_base + self.fallback_book_id
        """URL de fallback para o livro: `https://www.goodreads.com/book/show/{book_fallback}`"""

        self.search_results_html_path: Path = self.output_html_directory / "search_results.html"
        """Caminho do arquivo HTML da busca: `./data/html/search_results.html`"""

    def _log_and_raise_exception(
        self, error_message: str, exception_class: type[Exception]
    ) -> None:
        """Loga a mensagem de erro e lança a exceção especificada."""
        self.logger.exception(error_message)
        raise exception_class(error_message)

    def _handle_exceptions(self, error_message: str) -> None:
        """Método auxiliar para tratamento de exceções comuns."""
        self._log_and_raise_exception(error_message, GoodreadsScraperError)

    def _save_html(self, output_path: Path, html: str) -> None:
        """Salve o conteúdo HTML no caminho especificado."""
        try:
            output_path.write_text(html, encoding="utf-8")
            self.logger.info(f"HTML da busca salvo com sucesso em: '{output_path}'")
        except OSError:
            self._log_and_raise_exception(f"Erro ao salvar o HTML em '{output_path}'", OSError)

    def _get_search_results_response(self) -> httpx.Response:
        """Executa o GET na URL de pesquisa e valida as mensagens de retorno possíveis."""
        try:
            self.logger.info(f"Acessando URL de pesquisa: '{self.goodreads_search_url}'")
            with httpx.Client(timeout=20.0, follow_redirects=True) as client:
                response = client.get(self.goodreads_search_url)
                response.raise_for_status()
        except httpx.HTTPStatusError:
            self._log_and_raise_exception(
                (
                    f"Erro HTTP ao acessar a URL de pesquisa: {self.goodreads_search_url} "
                    f"— código de status HTTP inválido"
                ),
                httpx.HTTPStatusError,
            )
        except httpx.RequestError:
            self._log_and_raise_exception(
                (f"Erro de requisição ao acessar a URL de pesquisa: {self.goodreads_search_url}"),
                httpx.RequestError,
            )
        else:
            if not response.text or "Nenhum resultado encontrado" in response.text:
                msg = "Nenhum resultado encontrado na pesquisa do Goodreads."
                self.logger.warning(msg)
                raise GoodreadsScraperError(msg)
            return response

    def _download_search_results_html(self) -> Path:
        """Baixe o HTML da página de resultados de busca e salve localmente."""
        try:
            response = self._get_search_results_response()
            html = response.text
            self._save_html(self.search_results_html_path, html)
        except GoodreadsScraperError:
            self.logger.exception(super()._raise_error())
            raise
        else:
            self.logger.info("Busca no Goodreads realizada e HTML salvo com sucesso.")
            return self.search_results_html_path

    def _extract_first_book_link(self) -> str | None:
        """Extrai e limpa o link do primeiro livro dos resultados de busca."""
        try:
            html_path = self._download_search_results_html()
            soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")

            first_row = self._find_first_book_row(soup)
            if not first_row:
                return None

            first_link = self._find_first_link(first_row)
            if not first_link:
                return None

            clean_link = self._clean_link(first_link)
        except GoodreadsScraperError:
            self.logger.exception(super()._raise_error())
            raise
        else:
            self.logger.info(f"Link do primeiro livro extraído: '{clean_link}'")
            return clean_link

    def _find_first_book_row(self, soup: BeautifulSoup) -> Tag | None:
        """Encontra a primeira linha de livro nos resultados de busca."""
        first_row = soup.find("tr", {"itemscope": "", "itemtype": "http://schema.org/Book"})
        if not isinstance(first_row, Tag):
            self.logger.warning("Nenhum item encontrado na árvore especificada.")
            return None
        return first_row

    def _find_first_link(self, first_row: Tag) -> str | None:
        """Encontra o link do primeiro livro na linha especificada."""
        first_link = first_row.find("a", {"title": True})
        if not (isinstance(first_link, Tag) and first_link.has_attr("href")):
            self.logger.warning("Nenhum link válido encontrado no primeiro item.")
            return None
        return first_link.get("href")

    def _clean_link(self, href: str) -> str:
        """Limpa o link extraído, removendo parâmetros desnecessários."""
        raw_link = f"https://www.goodreads.com{href}"
        return raw_link.split("?", maxsplit=1)[0]

    def _get_filename_from_url(self, book_link: str) -> str:
        """Extrai o nome do arquivo a partir da URL do Goodreads."""
        if book_link.startswith(self.goodreads_book_url_base):
            return book_link[len(self.goodreads_book_url_base) :].rstrip("/") + ".html"
        return book_link.rstrip("/").split("/", maxsplit=1)[-1] + ".html"

    def _is_file_cache_valid(self, file_path: Path) -> bool:
        """Verifica se o arquivo existe e ainda está dentro do período de cache válido."""
        if not file_path.exists():
            self.logger.warning(f"Arquivo não encontrado: '{file_path}'")
            return False

        last_modified_time = datetime.fromtimestamp(file_path.stat().st_mtime, tz=BRT)
        current_time = datetime.now(tz=BRT)
        is_valid = (current_time - last_modified_time).total_seconds() < self.cache_duration_seconds

        if is_valid:
            self.logger.info(f"Cache válido encontrado: '{file_path}'")
        else:
            self.logger.info(f"Cache expirado ou inválido: '{file_path}'")

        return is_valid

    def _download_or_use_cache(self, book_link: str) -> Path:
        """Baixa o HTML ou utiliza o cache válido."""
        try:
            filename = self._get_filename_from_url(book_link)
            output_path = self.output_html_directory / filename

            if self._is_file_cache_valid(output_path):
                self.logger.info(f"Usando cache válido: '{output_path}'")
                return output_path

            # Realiza o download caso o cache não seja válido
            self.logger.info(f"Cache inválido ou inexistente. Baixando: '{book_link}'")
            with httpx.Client(timeout=20.0, follow_redirects=True) as client:
                response = client.get(book_link)
                response.raise_for_status()
                html = response.text

            output_path.write_text(html, encoding="utf-8")
            self.logger.info(f"HTML salvo em: '{output_path}'")

        except (httpx.HTTPStatusError, OSError):
            self._handle_exceptions(f"Erro ao processar o link: '{book_link}'.")
        else:
            return output_path

    def execute_download(self) -> Path:
        """Executa o processo de download de HTML e registra as atividades."""
        try:
            self.logger.info(f"Pesquisando livro no Goodreads: '{self.search_book_title}'")
            book_link = self._extract_first_book_link() or self.fallback_book_url
            html_path = self._download_or_use_cache(book_link)
            self.logger.info(f"HTML baixado com sucesso: '{html_path.name}'")
        except GoodreadsScraperError:
            self.logger.exception("Erro durante o download.")
            raise
        else:
            self.logger.info("Processo de download concluído.")
            return html_path
