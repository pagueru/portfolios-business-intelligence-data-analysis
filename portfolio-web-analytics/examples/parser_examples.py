"""Exemplos de uso da classe ParserRepository."""

import json
from pathlib import Path
import sys

import python_path

from src.repositories.parser_repository import ParserRepository


def example_extract_data_from_html() -> None:
    """Exemplo de extração de dados de um arquivo HTML usando ParserRepository."""
    html_path = Path("./data/html/25986929-goodnight-punpun-omnibus-vol-1.html")
    yaml_path = Path("./src/config/parser.yaml")

    # Inicializa o ParserRepository
    parser = ParserRepository(html_path)

    # Remove elementos desnecessários
    # parser.remove_svg_with_viewbox()

    # Extrai dados com base no arquivo YAML
    extracted_data = parser.extract_from_yaml(yaml_path)

    # Formata os dados extraídos para remover espaços e quebras de linha
    extracted_data = parser.format_extracted_data(extracted_data)

    # Exibe os dados extraídos e formatados
    print("Dados extraídos:", json.dumps(extracted_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    example_extract_data_from_html()
