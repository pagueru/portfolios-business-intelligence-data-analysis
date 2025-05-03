"""Orquestra a execução dos processos de extração de codeblocks e conversão Markdown para PDF."""

from src.codeblock_extractor import CodeblockExtractor
from src.core.logger import get_logger
from src.markdown_pdf import MarkdownToPdfConverter

MENU_OPTIONS = {
    "1": "Extrair codeblocks do Markdown",
    "2": "Converter Markdown em PDF",
    "0": "Sair",
}


class ProcessRunner:
    """Executa o processo selecionado pelo menu interativo."""

    def __init__(self) -> None:
        """Inicializa o logger do processo."""
        self.logger = get_logger(__name__)

    def print_terminal_line(self, value: int = 80, char: str = "-") -> None:
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
            self.logger.info("Iniciando o script.")
        except RuntimeError:
            self.logger.exception("Erro ao limpar o terminal.")

    def show_menu(self) -> str:
        """Exibe o menu e retorna a opção escolhida pelo usuário."""
        self.print_terminal_line()
        print("i Selecione uma opção:")
        for key, desc in MENU_OPTIONS.items():
            print(f"{key} - {desc}")
        return input("➔ Opção: ").strip()

    def _keyboard_exit(self) -> None:
        """Interrompe a execução em formato `KeyboardInterrupt`."""
        raise KeyboardInterrupt

    def run(self) -> None:
        """Executa o menu em loop até o usuário escolher sair."""
        self.start_config()
        try:
            while True:
                option = self.show_menu()
                if option == "1":
                    extractor = CodeblockExtractor(
                        md_path="./README.md",
                        output_dir="./querys",
                        codeblock_lang="javascript",
                    )
                    extractor.extract()
                elif option == "2":
                    converter = MarkdownToPdfConverter(
                        input_md="./README.md",
                        css_files=["./css/custom-github-markdown.css"],
                        html_output_path="./docs/README.html",
                        output_pdf="./docs/README.pdf",
                    )
                    converter.run()
                elif option == "0":
                    self._keyboard_exit()
                else:
                    print("✖ Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("0")
            self.print_terminal_line()
            self.logger.info("Execução interrompida pelo usuário.")


if __name__ == "__main__":
    runner = ProcessRunner()
    runner.run()
