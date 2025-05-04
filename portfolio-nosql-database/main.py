"""Orquestra a execução dos processos de extração de codeblocks e conversão Markdown para PDF."""

import sys

from src.codeblock_extractor import CodeblockExtractor
from src.core.logger import logger
from src.markdown_pdf import MarkdownToPdfConverter

MENU_OPTIONS = {
    "1": "Extrair codeblocks do Markdown",
    "2": "Converter Markdown em PDF",
    "0": "Finalizar",
}

# Constantes de configuração de caminhos e parâmetros
MD_PATH = "./README.md"
OUTPUT_DIR = "./querys"
CODEBLOCK_LANG = "javascript"
CSS_FILES = ["./css/custom-github-markdown-light.css"]
HTML_OUTPUT_PATH = "./docs/README.html"
OUTPUT_PDF = "./docs/relatorio-aula-pratica-3481350205.pdf"


class ProcessRunner:
    """Executa o processo selecionado pelo menu interativo."""

    def __init__(self) -> None:
        """Inicializa o logger do processo."""

    def print_terminal_line(self, value: int = 90, char: str = "-") -> None:
        """Imprime uma linha no terminal com o caractere especificado."""
        if value <= 0:
            msg = "O valor deve ser maior que 0."
            raise ValueError(msg)
        print(char * value)

    def start_config(self, *, clear_terminal: bool = True) -> None:
        """Limpa o terminal e marca o início do script."""
        try:
            if clear_terminal:
                print("\033[H\033[J", end="", flush=True)
            self.print_terminal_line()
            logger.info("Iniciando o script.")
        except RuntimeError:
            logger.exception("Erro ao limpar o terminal.")

    def show_menu(self) -> str:
        """Exibe o menu e retorna a opção escolhida pelo usuário."""
        self.print_terminal_line()
        print("Selecione uma opção:")
        for key, desc in MENU_OPTIONS.items():
            print(f"{key} - {desc}")
        return input("➔ Opção: ").strip()

    def run(self) -> None:
        """Executa o menu em loop até o usuário escolher sair."""
        self.start_config()
        try:
            while True:
                option = self.show_menu()
                if option == "1":
                    extractor = CodeblockExtractor(
                        md_path=MD_PATH,
                        output_dir=OUTPUT_DIR,
                        codeblock_lang=CODEBLOCK_LANG,
                    )
                    self.print_terminal_line()
                    extractor.extract()
                if option == "2":
                    converter = MarkdownToPdfConverter(
                        input_md=MD_PATH,
                        css_files=CSS_FILES,
                        html_output_path=HTML_OUTPUT_PATH,
                        output_pdf=OUTPUT_PDF,
                    )
                    self.print_terminal_line()
                    converter.run()
                if option == "0":
                    self.print_terminal_line()
                    logger.info("Execução interrompida pelo usuário.")
                    sys.exit()
                else:
                    print("✖ Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print()
            self.print_terminal_line()
            logger.info("Execução interrompida pelo usuário.")
        finally:
            self.print_terminal_line()


if __name__ == "__main__":
    runner = ProcessRunner()
    runner.run()
