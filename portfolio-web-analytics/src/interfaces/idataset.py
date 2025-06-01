"""Interface para download de datasets."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd


class IDatasetDownloader(ABC):
    """Interface para classes que baixam datasets."""

    @abstractmethod
    def download_dataset(self, *, force_download: bool = False) -> Path:
        """Baixa o dataset usando o serviço nativo."""

    @abstractmethod
    def load_as_dataframe(self, file_path: str = "") -> pd.DataFrame:
        """Carrega o dataset como DataFrame do pandas."""

    @abstractmethod
    def get_dataset_info(self, file_path: str = "") -> dict[str, Any]:
        """Retorna informações sobre o dataset."""
