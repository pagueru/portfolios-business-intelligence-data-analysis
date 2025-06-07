"""Implementação do downloader de datasets do Kaggle."""

from pathlib import Path
from typing import TYPE_CHECKING, Any

import duckdb
import kagglehub
import pandas as pd

from src.common.logger import LoggerSingleton
from src.core.base_class import BaseClass
from src.core.errors import KaggleDatasetError

if TYPE_CHECKING:
    from logging import Logger


class KaggleRepository(BaseClass):
    """Baixa datasets do Kaggle usando kagglehub."""

    def __init__(self, dataset_config: dict[str, Any]) -> None:
        self.logger: Logger = LoggerSingleton().logger or LoggerSingleton.get_logger()
        """Logger singleton para registrar eventos e erros."""

        self.manga_name: str = dataset_config["manga_name"]
        """Nome do manga a ser baixado. Ex.: `PunPun`"""

        self.dataset_name: str = dataset_config["dataset_name"]
        """Nome do dataset a ser baixado. Ex.: `duongtruongbinh/manga-and-anime-dataset`"""

        self.force_download: bool = dataset_config["force_download"]
        """Flag para forçar o download do dataset mesmo se já estiver em cache: `False`"""

        self.datasets_path: Path = Path("./data/datasets")
        """Caminho base onde os datasets serão armazenados localmente: `./data/datasets/`"""

        self.datasets_file: list[str] = dataset_config["dataset_files"]
        """Lista de arquivos do dataset a serem baixados. Ex.: `manga.csv`"""

    def _is_dataset_cached(self) -> bool:
        """Verifica se todos os arquivos do dataset já existem no cache local."""
        if not self.force_download and self.datasets_path.exists():
            cached_files = {file.name for file in self.datasets_path.iterdir()}
            missing_files = set(self.datasets_file) - cached_files

            if not missing_files:
                self.logger.info(
                    f"Todos os arquivos do dataset estão no cache local: '{self.datasets_path}'"
                )
                return True

            self.logger.info(f"Arquivos ausentes no cache local: '{missing_files}'")
        else:
            self.logger.info("Cache local não encontrado ou force_download está ativado.")

        return False

    def download_dataset(self) -> Path:
        """Baixa os arquivos do dataset especificados em datasets_file."""
        try:
            dataset_path = kagglehub.dataset_download(self.dataset_name)
            dataset_path = Path(dataset_path)
            self.datasets_path.mkdir(parents=True, exist_ok=True)

            for file in dataset_path.iterdir():
                if file.name in self.datasets_file:
                    dest = self.datasets_path / file.name
                    dest.write_bytes(file.read_bytes())
                    self.logger.info(f"Arquivo '{file.name}' copiado para o cache local.")
                else:
                    self.logger.info(f"Arquivo '{file.name}' ignorado.")
        except KaggleDatasetError:
            self.logger.exception("Erro inesperado ao baixar dataset")
            raise
        return self.datasets_path

    def load_dataframe(self, file_name: str) -> pd.DataFrame:
        """Carrega o arquivo especificado como um DataFrame."""
        file_path = self.datasets_path / file_name

        if not file_path.exists():
            self.download_dataset()

        try:
            dataframe = pd.read_csv(file_path)
            self.logger.info(f"Arquivo '{file_name}' carregado com sucesso.")
        except Exception as exc:
            msg = f"Erro ao carregar o arquivo '{file_name}'."
            self.logger.exception(msg)
            raise KaggleDatasetError(msg) from exc
        else:
            return dataframe

    def dataframe_to_json(self, dataframe: pd.DataFrame) -> dict | list[dict]:
        """Converte um DataFrame carregado para um dicionário ou uma lista de dicionários (JSON)."""
        try:
            json_data = dataframe.to_dict(orient="records")
            return json_data[0] if len(json_data) == 1 else json_data
        except Exception as exc:
            msg = "Erro ao converter DataFrame para JSON."
            self.logger.exception(msg)
            raise KaggleDatasetError(msg) from exc

    def filter_by_manga_name(
        self, dataframe: pd.DataFrame, column: str | None = None, manga_name: str | None = None
    ) -> pd.DataFrame:
        """Filtra o DataFrame pelo campo 'Title' com base na variável manga_name."""
        try:
            manga_name = manga_name if manga_name else self.manga_name
            filtered_df = dataframe[
                dataframe[column or "Title"].str.contains(manga_name, case=False, na=False)
            ]
        except KeyError as exc:
            msg = f"A coluna '{column}' não foi encontrada no DataFrame."
            self.logger.exception(msg)
            raise KaggleDatasetError(msg) from exc
        except Exception as exc:
            msg = f"Erro ao filtrar o DataFrame pelo manga: '{manga_name}'."
            self.logger.exception(msg)
            raise KaggleDatasetError(msg) from exc
        else:
            self.logger.info(f"Filtragem concluída para o manga: '{manga_name}'.")
            return filtered_df

    def filter_by_manga_name_with_duckdb(self, file_name: str) -> list[dict]:
        """Filtra o arquivo CSV pelo campo 'Title' com base na variável manga_name usando DuckDB."""
        file_path = self.datasets_path / file_name

        if not file_path.exists():
            msg = f"O arquivo '{file_name}' não foi encontrado no cache local."
            self.logger.error(msg)
            raise FileNotFoundError(msg)

        try:
            query = """
                SELECT *
                FROM read_csv_auto(?)
                WHERE Title LIKE ?
            """
            result: duckdb.DuckDBPyRelation = duckdb.query(
                query, (str(file_path), f"%{self.manga_name.lower()}%")
            )
            filtered_data = result.to_df().to_dict(orient="records")
        except Exception as exc:
            msg = (
                f"Erro ao filtrar o arquivo '{file_name}' pelo manga: '{self.manga_name}' "
                "usando DuckDB."
            )
            self.logger.exception(msg)
            raise KaggleDatasetError(msg) from exc
        else:
            self.logger.info(
                f"Filtragem concluída para o manga: '{self.manga_name}' usando DuckDB."
            )
            return filtered_data
