from bs4 import BeautifulSoup, Tag

from src.common.logger import LoggerSingleton
from src.core.errors import HTMLParserError


class CleanRepository:
    """Classe utilitária para limpeza de HTML do Goodreads."""

    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup
        self.logger = LoggerSingleton.logger or LoggerSingleton.get_logger()

    def remove_svg_with_viewbox(self) -> None:
        """Remove tags `<svg>` com atributo `viewBox` (case-insensitive) do HTML carregado."""
        removed = 0
        try:
            for svg in self.soup.find_all("svg"):
                if isinstance(svg, Tag) and svg.has_attr("viewbox"):
                    svg.decompose()
                    removed += 1
        except HTMLParserError:
            self.logger.exception("Erro ao remover tags '<svg>'.")
            raise
        else:
            if removed == 0:
                self.logger.debug(
                    "Nenhuma tag '<svg>' com atributo 'viewBox' ou 'viewbox' encontrada."
                )
            self.logger.debug(
                f"Removidas {removed} tags '<svg>' com atributo 'viewBox' ou 'viewbox'."
            )

    def keep_only_main_content(self) -> None:
        """Mantenha apenas o conteúdo da div 'BookPage__mainContent'."""
        try:
            main_content = self.soup.find("div", class_="BookPage__mainContent")
            if main_content is not None:
                new_soup = BeautifulSoup("<html><body></body></html>", "lxml")
                if new_soup.body is not None:
                    new_soup.body.insert(0, main_content.extract())
                    self.soup = new_soup
                else:
                    self.logger.warning(
                        "Body não encontrado no novo soup. Nenhuma alteração realizada."
                    )
            else:
                self.logger.debug(
                    "Div 'BookPage__mainContent' não encontrada. Nenhuma alteração realizada."
                )
        except HTMLParserError:
            self.logger.exception("Erro ao manter apenas o conteúdo principal.")
            raise
        else:
            self.logger.debug("Conteúdo principal mantido com sucesso.")
