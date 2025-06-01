"""Orquestrador principal: executa scraping, transformação e armazenamento."""

from contextlib import suppress
import json
import os
from pathlib import Path
from typing import Any

from repositories.goodreads import GoodreadsHTMLParser
from repositories.html_downloader import HTMLDownloader
from repositories.kaggle_downloader import KaggleDatasetDownloader
from src.common.echo import echo
from src.common.logger import LoggerSingleton
from src.common.utils import ProjectUtils
from src.core.errors import ProjectError

os.system("cls")  # noqa: S605, S607
logger = LoggerSingleton().logger or LoggerSingleton.get_logger()


class WebAnalyticsPipeline:
    """Classe principal para orquestrar o pipeline de web analytics."""

    def __init__(
        self,
        book_url: str,
        html_output_dir: Path,
        parser_config: Path,
        kaggle_dataset: str,
        results_file: Path,
    ):
        self.book_url = book_url
        self.html_output_dir = html_output_dir
        self.parser_config = parser_config
        self.kaggle_dataset = kaggle_dataset
        self.results_file = results_file
        self.project_utils = ProjectUtils()
        self.logger = LoggerSingleton().logger or LoggerSingleton.get_logger()

    def download_goodreads_html(self) -> Path:
        """Baixa o HTML de uma página do Goodreads e retorna o caminho do arquivo."""
        self.project_utils.separator_line()
        echo("Etapa 1 — Download do HTML do Goodreads", "arrow")

        html_downloader = HTMLDownloader(self.book_url, self.html_output_dir)
        html_path = html_downloader.get_or_download_html()
        echo(f"HTML baixado com sucesso: '{html_path.name}'", "success")
        return html_path

    def process_html_and_extract_data(self, html_path: Path) -> dict[str, Any]:
        """Processa o HTML baixado e extrai os dados usando o parser YAML."""
        self.project_utils.separator_line()
        echo("Etapa 2 — Processamento do HTML", "arrow")

        output_path = Path("./data/html/goodreads_books_full_clean.html")

        # Processamento do HTML
        parser = GoodreadsHTMLParser(html_path)
        parser.keep_only_main_content()
        parser.remove_svg_with_viewbox()
        parser.save_html(output_path)
        echo(f"HTML processado salvo em: '{output_path}'", "bullet")

        # Extração de dados
        return parser.extract_from_yaml(self.parser_config)

    def download_kaggle_dataset(self, dataset_downloader: KaggleDatasetDownloader) -> None:
        """Baixe o dataset do Kaggle, sem realizar análise."""
        self.project_utils.separator_line()
        echo("Etapa 3 — Download do dataset do Kaggle", "arrow")

        kaggle_downloader = dataset_downloader
        echo("Verificação de cache", "bullet")
        if kaggle_downloader.is_dataset_cached():
            echo("Dataset encontrado em cache local.", "bullet")
        else:
            echo("Dataset não encontrado em cache. Iniciando download...", "wait")

        kaggle_downloader.download_dataset()

    def analyze_manga_dataset(
        self, kaggle_downloader: KaggleDatasetDownloader
    ) -> dict[str, Any] | None:
        """Analisa especificamente o dataset de manga."""
        echo("Análise do dataset de manga", "bullet")
        manga_df = kaggle_downloader.load_as_dataframe("manga.csv")
        echo(f"Dados carregados: {len(manga_df)} registros de manga", "bullet")

        # Informações detalhadas do dataset de manga
        manga_info = kaggle_downloader.get_dataset_info("manga.csv")

        return {
            "records_count": len(manga_df),
            "columns": manga_df.columns.tolist(),
            "sample_data": manga_df.head().to_dict(),
            "dataset_info": manga_info,
        }

    def search_manga_in_dataset(
        self, kaggle_downloader: KaggleDatasetDownloader, manga_title: str
    ) -> dict[str, Any] | None:
        """Pesquisa um manga específico no dataset de manga."""
        echo(f"Pesquisa no dataset de manga: {manga_title}", "bullet")
        manga_df = kaggle_downloader.load_as_dataframe("manga.csv")

        # Filtrar o dataset pelo título do manga
        filtered_df = manga_df[manga_df["Title"].str.contains(manga_title, case=False, na=False)]
        if filtered_df.empty:
            self.logger.warning(f"Nenhum resultado encontrado para o manga: {manga_title}")
            return None

        echo(f"Resultados encontrados: {len(filtered_df)} registros", "bullet")

        return {
            "records_count": len(filtered_df),
            "sample_data": filtered_df.head().to_dict(),
        }

    def transform_manga_search_results(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Transforma os resultados brutos de pesquisa de manga em um formato desejado."""
        if not raw_data or "sample_data" not in raw_data:
            return {}

        sample_data = raw_data["sample_data"]
        transformed_data = {}

        for key, value in sample_data.items():
            # Extrai o primeiro valor do dicionário interno
            transformed_data[key] = next(iter(value.values()))

            # Converte strings de listas em listas reais
            if isinstance(transformed_data[key], str) and transformed_data[key].startswith("["):
                with suppress(json.JSONDecodeError):
                    transformed_data[key] = json.loads(transformed_data[key].replace("'", '"'))

        return transformed_data

    def save_pipeline_results(
        self, goodreads_data: dict[str, Any], manga_data: dict[str, Any] | None
    ) -> None:
        """Salva os resultados do pipeline em um arquivo JSON."""
        self.project_utils.separator_line()
        echo("Etapa 5 — Salvando resultados do pipeline", "arrow")

        results = {
            "goodreads": goodreads_data,
            "manga": manga_data or {},
        }

        with self.results_file.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False, default=str)

        echo(f"Resultados do pipeline salvos em: '{self.results_file}'", "bullet")

    def run(self) -> None:
        """Executa o pipeline principal de web analytics."""
        echo("Iniciando pipeline de web analytics", "info")

        # Criar diretórios se não existirem
        self.html_output_dir.mkdir(parents=True, exist_ok=True)
        self.results_file.parent.mkdir(parents=True, exist_ok=True)

        # Etapa 1: Download do HTML
        html_path = self.download_goodreads_html()

        # Etapa 2: Processamento e extração
        goodreads_data = self.process_html_and_extract_data(html_path)

        # Etapa 3: Pesquisa no dataset de manga
        kaggle_downloader = KaggleDatasetDownloader(self.kaggle_dataset)
        manga_search_results = self.search_manga_in_dataset(kaggle_downloader, "PunPun")

        # Etapa 4: Transformação dos resultados de pesquisa de manga
        if manga_search_results:
            manga_search_results = self.transform_manga_search_results(manga_search_results)

        # Salvar resultados combinados
        self.save_pipeline_results(goodreads_data, manga_search_results)

        # Log de resumo
        self.project_utils.separator_line()
        echo("Resumo da execução", "info")
        print(f"📚 Livro analisado: {goodreads_data.get('title', 'N/A')}")
        print(f"👤 Autor: {goodreads_data.get('autor', 'N/A')}")
        print(f"⭐ Rating: {goodreads_data.get('rating', 'N/A')}")

        self.project_utils.separator_line()
        echo("Pipeline executado com sucesso!", "success")


if __name__ == "__main__":
    try:
        pipeline = WebAnalyticsPipeline(
            book_url="https://www.goodreads.com/book/show/25986929-goodnight-punpun-omnibus-vol-1",
            html_output_dir=Path("./data/html"),
            parser_config=Path("./src/config/parser.yaml"),
            kaggle_dataset="duongtruongbinh/manga-and-anime-dataset",
            results_file=Path("./data/pipeline_results.json"),
        )
        pipeline.run()
    except KeyboardInterrupt:
        ProjectUtils().separator_line()
        echo("Pipeline interrompido pelo usuário.", "flag")
