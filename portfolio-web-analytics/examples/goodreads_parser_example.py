"""Exemplos de uso da classe ParserRepository."""

import json

import pathfix  # noqa: F401

from src.common.errors.errors import ProjectError
from src.config.constants import PARSER_FILE
from src.infrastructure.datasources.goodreads_parser import GoodreadsParser

try:
    # Inicializa o ParserRepository
    parser = GoodreadsParser()

    # Extrai dados com base no arquivo YAML
    extracted_data = parser.extract_from_yaml(PARSER_FILE)

    # Formata os dados extraídos para remover espaços e quebras de linha
    extracted_data = parser.format_extracted_data(extracted_data)

    # Exibe os dados extraídos e formatados
    print(json.dumps(extracted_data, indent=4, ensure_ascii=False))

except ProjectError as e:
    print(f"Erro ao processar o parser: {e}")
