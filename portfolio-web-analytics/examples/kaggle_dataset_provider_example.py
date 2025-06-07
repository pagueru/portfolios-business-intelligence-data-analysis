import json

import pathfix  # noqa: F401

from src.common.errors.errors import ProjectError
from src.config.settings_manager import SettingsManager
from src.infrastructure.datasources.kaggle_dataset_provider import KaggleDatasetProvider

try:
    # Instancia a classe de configuração do projeto
    config_repository = SettingsManager()

    # Instancia a classe KaggleRepository
    kaggle_repository = KaggleDatasetProvider(config_repository.kaggle_settings)

    # Faz o download do dataset do Kaggle
    kaggle_repository.download_dataset()

    # Carrega o arquivo CSV em um DataFrame
    manga_dataset = kaggle_repository.load_dataframe("manga.csv")

    # Filtra o DataFrame pelo nome do mangá "PunPun"
    manga_dataset = kaggle_repository.filter_by_manga_name(manga_dataset)

    # Converte o DataFrame filtrado para JSON
    manga_json = kaggle_repository.dataframe_to_json(manga_dataset)

    # Exibe o JSON formatado no console
    print(json.dumps(manga_json, indent=2, ensure_ascii=False))

except ProjectError as e:
    print(f"Erro ao processar o dataset: {e}")
