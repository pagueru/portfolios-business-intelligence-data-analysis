"""Orquestrador principal: executa scraping, transformação e armazenamento."""

from ast import literal_eval
import json
import re
from typing import TYPE_CHECKING, Any

from src.common.base.base_class import BaseClass
from src.common.echo import echo
from src.common.errors.errors import ProjectError
from src.config.constants import DATASETS_DIR, HTML_DIR, OUTPUT_DIR, PARSER_FILE
from src.config.settings_manager import SettingsManager
from src.infrastructure.datasources.goodreads_parser import GoodreadsParser
from src.infrastructure.datasources.goodreads_scraper import GoodreadsScraper
from src.infrastructure.datasources.kaggle_dataset_provider import KaggleDatasetProvider
from src.infrastructure.logger import LoggerSingleton

if TYPE_CHECKING:
    from logging import Logger


class WebAnalyticsPipeline(BaseClass):
    """Classe principal para orquestrar o pipeline de web analytics."""

    def __init__(
        self,
        config_repository: SettingsManager,
        goodreads_repository: GoodreadsScraper,
        kaggle_repository: KaggleDatasetProvider,
        parser_repository: GoodreadsParser,
    ):
        self.logger: Logger = LoggerSingleton.logger or LoggerSingleton.get_logger()
        """Logger singleton para registrar eventos e erros."""

        self.class_name = self.__class__.__name__
        """Nome da classe atual: `WebAnalyticsPipeline`"""

        self.parser_yaml_path = PARSER_FILE
        """Caminho do arquivo de configuração do parser, ex: `./src/config/parser.yaml`."""

        self.config_repository = config_repository
        """Repositório de configurações do projeto: `ConfigRepository`"""

        self.goodreads_repository = goodreads_repository
        """Repositório de scraping do Goodreads: `GoodreadsRepository`"""

        self.kaggle_repository = kaggle_repository
        """Repositório de scraping do Kaggle: `KaggleRepository`"""

        self.parser_repository = parser_repository
        """Repositório de parsing de HTML: `ParserRepository`"""

        self.datasets_directory = DATASETS_DIR
        """Diretório onde os datasets serão armazenados, ex: `./data/datasets.`"""

        self.html_directory = HTML_DIR
        """Diretório onde os arquivos HTML serão salvos, ex: `./data/html.`"""

        self.output_directory = OUTPUT_DIR
        """Diretório onde os resultados do pipeline serão salvos, ex: `./data/output.`"""

        self.output_path = self.output_directory / "pipeline_results.json"
        """Caminho do arquivo de saída do pipeline, ex: `./data/output/pipeline_results.json`."""

    def _abort_pipeline(self, msg: str) -> None:
        self.logger.error(msg)
        raise FileNotFoundError(msg)

    def _clean_number(self, text: str) -> int:
        return int(re.sub(r"[^\d]", "", text))

    def parse_goodreads(self, data: dict[str, Any]) -> dict[str, Any]:
        """Normaliza e converte os campos extraídos do Goodreads para tipos corretos."""
        return {
            "title": data["title"],
            "author": data["autor"],
            "pages": int(data["paperback"].split()[0]),
            "publication": data["publication"],
            "ratings_count": self._clean_number(data["ratings_count"]),
            "reviews": self._clean_number(data["reviews"]),
            "rating": float(data["rating"]),
            "author_books": int(re.findall(r"\d+", data["autor_stats"])[0]),
            "author_followers": int(re.findall(r"\d+", data["autor_stats"])[1]),
            "author_bio": data["author_bio"],
            "description": data["description"],
        }

    def parse_kaggle(self, data: dict[str, Any]) -> dict[str, Any]:
        """Normaliza e converte os campos extraídos do Kaggle para tipos corretos."""
        return {
            "title": data["Title"],
            "score": data["Score"],
            "vote": data["Vote"],
            "ranked": data["Ranked"],
            "popularity": data["Popularity"],
            "members": self._clean_number(data["Members"]),
            "favorite": self._clean_number(data["Favorite"]),
            "volumes": int(data["Volumes"]),
            "chapters": int(data["Chapters"]),
            "status": data["Status"],
            "published": data["Published"],
            "genres": literal_eval(data["Genres"]),
            "themes": literal_eval(data["Themes"]),
            "demographics": literal_eval(data["Demographics"]),
            "serialization": data["Serialization"],
            "author": data["Author"],
        }

    def run(self) -> None:
        """Executa o pipeline completo: scraping, parsing, análise e exportação dos dados."""
        import time

        self.logger.info("Iniciando pipeline de web analytics.")

        try:
            # 1. Validar configurações essenciais
            self.logger.info("Validando configurações do projeto.")
            self.config_repository.verify_settings(self.config_repository.settings)

            if not self.parser_yaml_path.exists():
                self._abort_pipeline(
                    f"Arquivo de configuração parser.yaml não encontrado: {self.parser_yaml_path}"
                )

            # 2. Baixar HTML do Goodreads
            self.logger.info("Executando scraping do Goodreads.")
            html_path = self.goodreads_repository.execute_download()
            if not html_path.exists():
                self._abort_pipeline(f"HTML não encontrado após download: {html_path}")

            # 3. Esperar o arquivo HTML realmente existir (sincronização)
            self.logger.info("Aguardando o arquivo HTML ser gerado...")
            timeout = 30  # segundos
            waited = 0
            while not html_path.exists() and waited < timeout:
                time.sleep(1)
                waited += 1
            if not html_path.exists():
                self._abort_pipeline(
                    f"Arquivo HTML '{html_path}' não foi encontrado após {timeout}s."
                )

            # 4. Extrair e formatar dados do HTML
            self.logger.info("Extraindo e formatando dados do HTML.")
            parser = GoodreadsParser(html_path)
            extracted_data = parser.run_full_extraction(self.parser_yaml_path)
            goodreads_normalized = self.parse_goodreads(extracted_data)
            self.logger.info("Dados extraídos e normalizados do Goodreads com sucesso.")

            # 5. Baixar e processar dataset do Kaggle
            self.logger.info("Baixando e processando dataset do Kaggle.")
            self.kaggle_repository.download_dataset()
            manga_file = self.config_repository.kaggle_settings["dataset_files"][0]
            manga_dataframe = self.kaggle_repository.load_dataframe(manga_file)
            filtered_dataframe = self.kaggle_repository.filter_by_manga_name(manga_dataframe)
            kaggle_json = self.kaggle_repository.dataframe_to_json(filtered_dataframe)
            if isinstance(kaggle_json, list) and kaggle_json:
                kaggle_normalized = self.parse_kaggle(kaggle_json[0])
            else:
                kaggle_normalized = self.parse_kaggle(kaggle_json)
            self.logger.info("Dados do Kaggle processados e normalizados com sucesso.")

            # 6. Unir dados extraídos
            pipeline_result = {
                "goodreads": goodreads_normalized,
                "kaggle": kaggle_normalized,
            }

            # 7. Salvar resultado final
            with self.output_path.open("w", encoding="utf-8") as file:
                json.dump(pipeline_result, file, ensure_ascii=False, indent=2)
            self.logger.info(f"Resultado da pipeline salvo em: '{self.output_path}'")
            super()._separator_line()
            echo(
                f"Pipeline finalizado com sucesso. Resultado salvo em: '{self.output_path}'",
                "success",
            )

        except ProjectError:
            self.logger.exception("Erro durante a execução do pipeline.")
            raise
