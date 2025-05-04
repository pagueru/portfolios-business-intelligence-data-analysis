"""Converte README.md em PDF aplicando estilos GitHub Markdown (claro e escuro)."""

from collections.abc import Sequence
from pathlib import Path
import subprocess

from weasyprint import HTML

from src.core.logger import logger


class MarkdownToPdfConverter:
    """Encapsula a conversão de Markdown para PDF com estilos customizados."""

    def __init__(
        self,
        input_md: str,
        css_files: Sequence[str],
        html_output_path: str,
        output_pdf: str,
    ) -> None:
        """Inicializa os caminhos e arquivos de conversão."""
        self.input_md = Path(input_md)
        self.css_files = [Path(css) for css in css_files]
        self.html_output_path = Path(html_output_path)
        self.output_pdf = Path(output_pdf)

    def convert_md_to_html(self) -> None:
        """Converte arquivo Markdown em HTML aplicando CSS customizado."""
        logger.info(f"Convertendo {self.input_md} para HTML com estilos {self.css_files}...")
        pandoc_cmd: list[str] = [
            "pandoc",
            str(self.input_md),
            "--standalone",
            "--highlight-style=pygments",
        ]
        for css in self.css_files:
            pandoc_cmd.extend(["--css", str(css)])
        pandoc_cmd.extend(["--resource-path=.", "-o", str(self.html_output_path)])
        try:
            subprocess.run(pandoc_cmd, check=True)  # noqa: S603
        except subprocess.CalledProcessError:
            logger.exception("Erro ao converter Markdown para HTML")
            raise

    def convert_html_to_pdf(self) -> None:
        """Converte arquivo HTML em PDF usando WeasyPrint."""
        logger.info(f"Convertendo {self.html_output_path} para PDF...")
        try:
            HTML(str(self.html_output_path), base_url=".").write_pdf(str(self.output_pdf))
            logger.info(f"PDF gerado com sucesso: {self.output_pdf}")
        except Exception:
            logger.exception("Erro ao converter HTML para PDF.")
            raise

    def run(self) -> None:
        """Executa o fluxo completo de conversão Markdown → HTML → PDF."""
        self.convert_md_to_html()
        self.convert_html_to_pdf()
