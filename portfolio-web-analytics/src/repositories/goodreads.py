"""Lógica de scraping específica para buscas e detalhes de livros no Goodreads."""

from collections.abc import Mapping
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from bs4 import BeautifulSoup, Tag
import yaml

from src.common.logger import LoggerSingleton
from src.core.errors import HTMLParserError

if TYPE_CHECKING:
    from src.config.constypes import ParserDict


class GoodreadsHTMLParser:
    """Realize o parsing de arquivos HTML do Goodreads e extraia elementos conforme solicitado."""

    def __init__(self, html_path: Path) -> None:
        """Inicializa a classe."""
        self.html_path = html_path
        self.logger = LoggerSingleton().logger or LoggerSingleton.get_logger()
        self.soup = self._load_html()

    def _load_html(self) -> BeautifulSoup:
        """Carrega e parseia o HTML usando BeautifulSoup."""
        self.logger.debug(f"Lendo arquivo HTML: {self.html_path}")
        html = self.html_path.read_text(encoding="utf-8")
        return BeautifulSoup(html, "lxml")

    def remove_svg_with_viewbox(self) -> None:
        """Remove tags <svg> com atributo 'viewBox' (case-insensitive) do HTML carregado."""
        removed = 0
        for svg in self.soup.find_all("svg"):
            if isinstance(svg, Tag) and svg.has_attr("viewbox"):
                svg.decompose()
                removed += 1
        self.logger.debug(f"Removidas {removed} tags <svg> com atributo 'viewBox' ou 'viewbox'.")

    def extract_from_yaml(self, yaml_path: Path) -> dict[str, Any]:
        """Extrai dados de um arquivo YAML e busca elementos no HTML carregado."""
        with yaml_path.open(encoding="utf-8") as file:
            config: ParserDict = yaml.safe_load(file)
        result: dict[str, Any] = {}

        for field, find_args in config.items():
            if not isinstance(find_args, dict):
                self.logger.warning(f"Configuração para o campo '{field}' não encontrada.")
                continue

            search_scope = self._get_search_scope(find_args)
            if search_scope:
                result[field] = self._extract_field_data(search_scope, field, find_args)

        return result

    def _get_search_scope(self, find_args: dict[str, Any]) -> BeautifulSoup:
        """Determina o escopo de busca baseado nos argumentos do YAML."""
        parent_args: dict[str, Any] | None = find_args.get("parent")
        search_scope = self.soup

        if parent_args:
            parent_name = parent_args.get("name")
            parent_attrs = parent_args.get("attrs", {})

            if isinstance(parent_name, str) and isinstance(parent_attrs, dict):
                parent_element = self.soup.find(parent_name, parent_attrs)
                search_scope = (
                    BeautifulSoup(str(parent_element), "lxml") if parent_element else self.soup
                )
            else:
                self.logger.warning("Atributos inválidos para o escopo de busca.")

        return search_scope

    def _extract_field_data(
        self, search_scope: BeautifulSoup, field: str, find_args: dict[str, Any]
    ) -> Any:
        """Extrai os dados de um campo específico baseado nos argumentos do YAML."""
        name = find_args.get("name")
        attrs = find_args.get("attrs", {})
        index = find_args.get("index")

        if isinstance(name, str) and isinstance(attrs, dict):
            elements = search_scope.find_all(name, attrs)

            if isinstance(elements, list) and elements:
                selected_element = (
                    elements[index]
                    if index is not None and isinstance(index, int) and index < len(elements)
                    else elements[0]
                )
                return selected_element.get_text(strip=True) if selected_element else None

        self.logger.warning(f"Atributos inválidos para o campo '{field}'.")
        return None

    def keep_only_main_content(self) -> None:
        """Mantenha apenas o conteúdo da div 'BookPage__mainContent'."""
        main_content = self.soup.find("div", class_="BookPage__mainContent")
        if main_content is not None:
            # Crie um novo soup apenas com o main_content
            new_soup = BeautifulSoup("<html><body></body></html>", "lxml")
            if new_soup.body is not None:
                new_soup.body.insert(0, main_content.extract())
                self.soup = new_soup
                self.logger.debug("Mantido apenas o conteúdo de 'BookPage__mainContent'.")
            else:
                self.logger.warning(
                    "Body não encontrado no novo soup. Nenhuma alteração realizada."
                )
        else:
            self.logger.debug(
                "Div 'BookPage__mainContent' não encontrada. Nenhuma alteração realizada."
            )

    def save_html(self, output_path: Path) -> None:
        """Salve o HTML atual (após modificações) em um novo arquivo."""
        soup_formatted = str(self.soup.prettify())
        output_path.write_text(soup_formatted, encoding="utf-8")
        self.logger.debug(f"HTML salvo em {output_path}")

    def export_to_json(
        self, data: dict[str, str | None], output_path: Path, *, indent: int = 2
    ) -> None:
        """Exporte os dados extraídos para um arquivo JSON."""
        with output_path.open("w", encoding="utf-8") as file:
            json.dump([data], file, ensure_ascii=False, indent=indent)
        self.logger.debug(f"Dados exportados para {output_path}")
