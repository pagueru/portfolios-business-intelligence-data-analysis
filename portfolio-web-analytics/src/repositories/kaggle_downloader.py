"""Implementação do downloader de datasets do Kaggle."""

import datetime
from pathlib import Path
from typing import Any

import chardet
import kagglehub
import pandas as pd

from interfaces.idataset import IDatasetDownloader
from src.common.logger import LoggerSingleton
from src.core.errors import KaggleDatasetError


class KaggleDatasetDownloader(IDatasetDownloader):
    """Baixa datasets do Kaggle usando kagglehub."""

    def __init__(self, dataset_name: str) -> None:
        """Inicializa o downloader com o nome do dataset."""
        self.dataset_name = dataset_name
        self.logger = LoggerSingleton().logger or LoggerSingleton.get_logger()
        self._cached_path: Path | None = None

    def is_dataset_cached(self) -> bool:
        """Verifica se o dataset já foi baixado anteriormente."""
        # Verifica cache local primeiro
        local_data_path = Path("data") / "datasets" / self.dataset_name.replace("/", "_")
        if local_data_path.exists() and any(local_data_path.iterdir()):
            self._cached_path = local_data_path
            self.logger.debug(f"Dataset encontrado em cache local: {local_data_path}")
            self._copy_to_local_cache(local_data_path)
            return True

        # Verifica cache do kagglehub
        try:
            test_path = kagglehub.dataset_download(self.dataset_name)
            self._cached_path = Path(test_path)
            self.logger.debug(f"Dataset encontrado em cache do kagglehub: {test_path}")
            self._copy_to_local_cache(Path(test_path))
        except (OSError, ImportError):
            self.logger.debug(f"Dataset não encontrado em cache: {self.dataset_name}")
            return False
        else:
            return True

    def download_dataset(self, *, force_download: bool = False) -> Path:
        """Baixa o dataset do Kaggle usando o cache nativo do kagglehub."""
        if not force_download and self.is_dataset_cached() and self._cached_path:
            self.logger.debug(f"Usando dataset do cache: {self._cached_path}")
            return self._cached_path

        self.logger.debug(f"Baixando dataset do Kaggle: {self.dataset_name}")

        try:
            # O kagglehub baixa automaticamente para seu cache interno
            dataset_path = kagglehub.dataset_download(self.dataset_name)
            dataset_path_obj = Path(dataset_path)

            # Copia para ./data/datasets/<nome_dataset>
            local_data_path = self._copy_to_local_cache(dataset_path_obj)
            self.logger.debug(f"Dataset copiado para: {local_data_path}")

        except Exception as exc:
            self.logger.exception(f"Erro ao baixar dataset do Kaggle: {self.dataset_name}")
            raise KaggleDatasetError from exc
        else:
            return local_data_path

    def _copy_to_local_cache(self, source_path: Path) -> Path:
        """Copia os arquivos do dataset diretamente para a pasta ./data/datasets."""
        local_data_path = Path("data") / "datasets"
        local_data_path.mkdir(parents=True, exist_ok=True)

        for file in source_path.iterdir():
            if file.is_file():
                dest = local_data_path / file.name
                dest.write_bytes(file.read_bytes())

        return local_data_path

    def load_as_dataframe(self, file_path: str = "") -> pd.DataFrame:
        """Carrega o dataset como DataFrame do pandas com detecção automática de encoding."""
        self.logger.debug(
            f"Carregando dataset como DataFrame: {self.dataset_name}, arquivo: {file_path}"
        )

        # Prioriza o uso do arquivo local na pasta ./data/datasets
        local_data_path = Path("data") / "datasets" / self.dataset_name.replace("/", "_")
        csv_file_path = local_data_path / file_path

        if not csv_file_path.exists():
            self.logger.debug(f"Arquivo não encontrado em cache local: {csv_file_path}")
            dataset_path = self.download_dataset(force_download=True)
            csv_file_path = dataset_path / file_path

        encoding = self._detect_encoding(csv_file_path)
        self.logger.debug(f"Encoding detectado: {encoding}")
        try:
            dataset_dataframe = pd.read_csv(csv_file_path, encoding=encoding)
            self.logger.debug(f"Dataset carregado com sucesso usando encoding: {encoding}")
            self.logger.debug(
                f"Dataset carregado com {len(dataset_dataframe)} registros e "
                f"{len(dataset_dataframe.columns)} colunas"
            )

        except pd.errors.ParserError as e:
            self.logger.exception(
                f"Erro de parsing ao carregar DataFrame: {self.dataset_name}/{file_path}"
            )
            msg = (
                f"Falha ao carregar DataFrame para '{self.dataset_name}/{file_path}'. "
                "Verifique se o arquivo está no formato CSV válido e se o delimitador está correto."
            )
            raise KaggleDatasetError(msg) from e
        except Exception as e:
            self.logger.exception(f"Erro ao carregar DataFrame: {self.dataset_name}/{file_path}")
            msg = f"Falha ao carregar DataFrame para '{self.dataset_name}/{file_path}'"
            raise KaggleDatasetError(msg) from e
        else:
            return dataset_dataframe

    def _detect_encoding(self, file_path: Path) -> str:
        """Detecta o encoding de um arquivo usando chardet com fallbacks."""
        try:
            detected_encoding = self._get_chardet_encoding(file_path)
            return self._validate_encoding(file_path, detected_encoding)
        except Exception as e:
            self.logger.exception(f"Erro durante detecção de encoding para {file_path}")
            msg = f"Falha na detecção de encoding para '{file_path}'"
            raise KaggleDatasetError(msg) from e

    def _get_chardet_encoding(self, file_path: Path) -> str:
        """Obtém o encoding detectado pelo chardet."""
        with file_path.open("rb") as file:
            raw_sample = file.read(10240)  # Primeiros 10KB

        detection = chardet.detect(raw_sample)
        detected_encoding = detection.get("encoding", "utf-8")
        detected_encoding = detected_encoding.lower() if detected_encoding else "utf-8"
        confidence = detection.get("confidence", 0.0)
        self.logger.debug(
            f"Chardet detectou encoding: {detected_encoding} (confiança: {confidence:.2f})"
        )
        return detected_encoding

    def _validate_encoding(self, file_path: Path, detected_encoding: str) -> str:
        """Valida o encoding testando diferentes opções."""
        encoding_fallbacks = [
            detected_encoding,
            "utf-8",
            "iso-8859-1",
            "windows-1252",
            "cp1252",
            "latin1",
        ]

        # Remove duplicatas mantendo ordem
        unique_encodings = list(dict.fromkeys(filter(None, encoding_fallbacks)))

        for encoding in unique_encodings:
            if self._test_encoding(file_path, encoding):
                self.logger.debug(f"Encoding {encoding} funcionou corretamente")
                return encoding
            self.logger.debug(f"Encoding {encoding} falhou")

        msg = f"Nenhum encoding funcionou para {file_path}. Encodings testados: {unique_encodings}"
        raise KaggleDatasetError(msg)

    def _test_encoding(self, file_path: Path, encoding: str) -> bool:
        """Testa se um encoding funciona para o arquivo."""
        try:
            pd.read_csv(file_path, encoding=encoding, nrows=1)
        except (UnicodeDecodeError, UnicodeError):
            return False
        else:
            return True

    def get_dataset_info(self, file_path: str = "") -> dict[str, Any]:
        """Retorna informações sobre o dataset."""
        # Remove try/except desnecessário - deixa a exceção propagar
        dataset_dataframe = self.load_as_dataframe(file_path)

        info = {
            "dataset_name": self.dataset_name,
            "file_path": file_path,
            "total_rows": len(dataset_dataframe),
            "total_columns": len(dataset_dataframe.columns),
            "columns": list(dataset_dataframe.columns),
            "data_types": dataset_dataframe.dtypes.to_dict(),
            "memory_usage": dataset_dataframe.memory_usage(deep=True).sum(),
            "last_checked": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        }

        self.logger.debug(f"Informações do dataset obtidas para: {self.dataset_name}")
        return info

    def preview_data(self, file_path: str = "", n_rows: int = 5) -> pd.DataFrame:
        """Carrega uma prévia do dataset com número limitado de linhas."""
        # Remove try/except desnecessário - deixa a exceção propagar
        dataset_dataframe = self.load_as_dataframe(file_path)
        preview = dataset_dataframe.head(n_rows)

        self.logger.debug(f"Prévia do dataset carregada: {n_rows} linhas")
        return preview
