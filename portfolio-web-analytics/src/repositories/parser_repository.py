"""Lógica de scraping específica para buscas e detalhes de livros no Goodreads."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from bs4 import BeautifulSoup, Tag
import yaml

from src.common.logger import LoggerSingleton
from src.core.base_class import BaseClass
from src.core.errors import HTMLParserError

if TYPE_CHECKING:
    from logging import Logger

    from src.config.constypes import ParserDict


class ParserRepository(BaseClass):
    """Realize o parsing de arquivos HTML do Goodreads e extraia elementos conforme solicitado."""

    def __init__(self, html_path: Path | None = None) -> None:
        self.logger: Logger = LoggerSingleton.logger or LoggerSingleton.get_logger()
        """Logger singleton para registrar eventos e erros."""

        self.html_path = (
            html_path if html_path else "./data/html/25986929-goodnight-punpun-omnibus-vol-1.html"
        )
        """Caminho do arquivo HTML a ser carregado."""

        self.soup: BeautifulSoup | None = None
        """BeautifulSoup será inicializado apenas quando necessário."""

    def _ensure_soup(self) -> None:
        """Garante que o BeautifulSoup foi inicializado com o HTML correto."""
        if self.soup is None:
            self.soup = super()._load_html(self.html_path)

    def _log_and_raise_exception(
        self, error_message: str, exception_class: type[Exception]
    ) -> None:
        """Loga a mensagem de erro e lança a exceção especificada."""
        self.logger.exception(error_message)
        raise exception_class(error_message)

    def extract_from_yaml(self, yaml_path: Path) -> dict[str, Any]:
        """Extrai dados de um arquivo YAML e busca elementos no HTML carregado."""
        try:
            self._ensure_soup()
            config: dict[str, Any] = self._load_yaml(yaml_path)
            result: dict[str, Any] = {}

            for field, find_args in config.items():
                if not isinstance(find_args, dict):
                    self.logger.warning(f"Configuração para o campo '{field}' não encontrada.")
                    continue

                search_scope = self._get_search_scope(find_args)
                if search_scope:
                    result[field] = self._extract_field_data(search_scope, field, find_args)

        except HTMLParserError:
            self._log_and_raise_exception("Erro ao extrair dados do arquivo YAML.", HTMLParserError)
        else:
            self.logger.debug("Dados extraídos com sucesso do arquivo YAML.")
            return result

    def _get_search_scope(self, find_args: dict[str, Any]) -> BeautifulSoup:
        """Determina o escopo de busca baseado nos argumentos do YAML."""
        try:
            self._ensure_soup()
            parent_args: dict[str, Any] | None = find_args.get("parent")
            search_scope = self.soup

            if parent_args:
                parent_name = parent_args.get("name")
                parent_attrs = parent_args.get("attrs")

                if isinstance(parent_name, str) and isinstance(parent_attrs, dict):
                    parent_element = self.soup.find(parent_name, parent_attrs)
                    search_scope = (
                        BeautifulSoup(str(parent_element), "lxml") if parent_element else self.soup
                    )
                else:
                    self.logger.warning("Atributos inválidos para o escopo de busca.")

        except HTMLParserError:
            self._log_and_raise_exception("Erro ao determinar o escopo de busca.", HTMLParserError)
        else:
            self.logger.debug("Escopo de busca determinado com sucesso.")
            return search_scope

    def _extract_field_data(
        self, search_scope: BeautifulSoup, field: str, find_args: dict[str, Any]
    ) -> Any:
        """Extrai os dados de um campo específico baseado nos argumentos do YAML."""
        try:
            name = find_args.get("name")
            attrs = find_args.get("attrs", {})
            index = find_args.get("index")

            # Lógica especial para author_bio:
            # busca global por todos os divs corretos e pega o primeiro span.Formatted não vazio
            if field == "author_bio":
                parent_args = find_args.get("parent")
                if parent_args:
                    parent_name = parent_args.get("name")
                    parent_attrs = parent_args.get("attrs", {})
                    # Busca global por todos os divs
                    parent_blocks = self.soup.find_all(parent_name, parent_attrs)
                    for block in parent_blocks:
                        span = block.find(name, attrs)
                        if span:
                            text = span.get_text(separator=" ", strip=True)
                            if text:
                                self.logger.debug("Biografia do autor extraída com sucesso.")
                                return text
                    self.logger.warning("Nenhuma biografia encontrada para o autor.")
                    return None

            if isinstance(name, str) and isinstance(attrs, dict):
                elements = search_scope.find_all(name, attrs)
                if isinstance(elements, list) and elements:
                    selected_element = (
                        elements[index]
                        if index is not None and isinstance(index, int) and index < len(elements)
                        else elements[0]
                    )
                    self.logger.debug(f"Dados extraídos com sucesso para o campo '{field}'.")
                    return selected_element.get_text(strip=True) if selected_element else None
                self.logger.warning(f"Nenhum elemento encontrado para o campo '{field}'.")
                return None
            self.logger.warning(f"Atributos inválidos para o campo '{field}'.")

        except HTMLParserError:
            self._log_and_raise_exception(
                f"Erro ao extrair dados do campo '{field}'.",
                HTMLParserError,
            )

    def format_extracted_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Formata todos os campos de texto do dicionário extraído."""
        formatted = {}
        for key, value in data.items():
            if isinstance(value, str):
                formatted[key] = " ".join(value.replace("\n", " ").split())
            else:
                formatted[key] = value
        return formatted

    def run_full_extraction(self, yaml_path: Path) -> dict[str, Any]:
        """Executa o processo completo de extração e formatação dos dados do HTML."""
        extracted = self.extract_from_yaml(yaml_path)
        return self.format_extracted_data(extracted)
