import json
from pathlib import Path
import sys

import python_path

from src.core.errors import ProjectError
from src.repositories.config_repository import ConfigRepository
from src.repositories.kaggle_repository import KaggleRepository

# Configuração do dataset
manual_config = {
    "dataset_name": "duongtruongbinh/manga-and-anime-dataset",
    "dataset_files": ["manga.csv", "anime.csv"],
    "force_download": False,
}

# Adicionando a classe de configuração do projeto
config_repository = ConfigRepository()

# Instancia a classe KaggleRepository
# kaggle_repository = KaggleRepository(manual_config)
kaggle_repository = KaggleRepository(config_repository.kaggle_settings)

manga_file = "./data/datasets/manga.csv"

duckdb_query = f"""
    SELECT *
      FROM read_csv_auto('{manga_file}')
     WHERE Title LIKE ?
"""

# Chamando o método principal para realizar o download
try:
    kaggle_repository.download_dataset()
    manga_dataset = kaggle_repository.load_dataframe("manga.csv")
    manga_dataset = kaggle_repository.filter_by_manga_name(manga_dataset, manga_name="PunPun")
    manga_json = kaggle_repository.dataframe_to_json(manga_dataset)
    print(json.dumps(manga_json, indent=2, ensure_ascii=False))
    # kaggle_repository.filter_by_manga_name_with_duckdb(file_name="manga.csv")
except ProjectError as e:
    print(f"Erro ao processar o dataset: {e}")
