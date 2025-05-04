"""Extrai codeblocks de um arquivo markdown e gera arquivos na pasta de saída."""

from pathlib import Path
import re

from src.core.logger import logger


class CodeblockExtractor:
    """Gerencia a extração de codeblocks de arquivos markdown."""

    def __init__(self, md_path: str, output_dir: str, codeblock_lang: str = "javascript") -> None:
        """Inicializa os caminhos e o tipo de codeblock a ser extraído."""
        self.md_path = Path(md_path)
        self.output_dir = Path(output_dir)
        self.codeblock_lang = codeblock_lang

    def read_codeblocks(self) -> list[tuple[str, str]]:
        """Lê o arquivo markdown e retorna uma lista de tuplas (nome, código)."""
        content = self.md_path.read_text(encoding="utf-8")
        pattern = re.compile(rf"```{self.codeblock_lang}\s*//\s*(\S+)\s*\n(.*?)```", re.DOTALL)
        return pattern.findall(content)

    def check_existing_files(self, matches: list[tuple[str, str]]) -> set[str]:
        """Verifica quais arquivos já existem na pasta de saída."""
        existing = set()
        for name, _ in matches:
            filename = name.strip()
            if not filename.endswith(".js"):
                filename = f"{filename}.js"
            file_path = self.output_dir / filename
            if file_path.exists():
                existing.add(filename)
        return existing

    def save_codeblocks(
        self, matches: list[tuple[str, str]], *, overwrite: bool = False
    ) -> tuple[int, int, int]:
        """Salva os codeblocks extraídos, controlando criação, substituição e ignorados."""
        created = 0
        replaced = 0
        ignored = 0
        for name, code in matches:
            filename = name.strip()
            if not filename.endswith(".js"):
                filename = f"{filename}.js"
            file_path = self.output_dir / filename
            header = f"// {filename}\n"
            file_content = f"{header}{code.strip()}\n"
            if file_path.exists():
                if overwrite:
                    file_path.write_text(file_content, encoding="utf-8")
                    logger.debug(f"Arquivo substituído: {file_path}")
                    replaced += 1
                else:
                    logger.debug(f"Arquivo ignorado (já existe): {file_path}")
                    ignored += 1
            else:
                file_path.write_text(file_content, encoding="utf-8")
                logger.debug(f"Arquivo criado: {file_path}")
                created += 1
        return created, replaced, ignored

    def extract(self, *, confirm: bool = True) -> None:
        """Executa o fluxo principal de extração e salvamento dos codeblocks."""
        if not self.md_path.exists():
            logger.error(f"Arquivo {self.md_path} não encontrado.")
            return
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
            logger.info(f"Diretório {self.output_dir} criado.")
        logger.info("Iniciando extração de codeblocks do arquivo Markdown.")
        matches = self.read_codeblocks()
        total_files = len(matches)
        if not matches:
            logger.warning("Nenhum codeblock encontrado.")
            logger.warning(f"Arquivo pesquisado: {self.md_path}.")
            return
        logger.info(f"Foram encontrados {total_files} codeblocks para extração.")
        if confirm:
            resposta = input(
                f"➔ Deseja gerar arquivos para os {total_files} codeblocks encontrados? "
                f"(1 = sim, 0 = não): "
            )
            if resposta.strip() != "1":
                logger.info("Execução abortada pelo usuário.")
                return
        existing = self.check_existing_files(matches)
        overwrite = True
        if existing and confirm:
            logger.info(f"{len(existing)} arquivos já existem na pasta de saída.")
            resposta = input(
                f"➔ {len(existing)} arquivos já existem. Deseja substituir? (1 = sim, 0 = não): "
            )
            overwrite = resposta.strip() == "1"
            if not overwrite:
                logger.info("Arquivos existentes serão ignorados.")
        created, replaced, ignored = self.save_codeblocks(matches, overwrite=overwrite)
        logger.info(f"Total de arquivos criados: {created}")
        logger.info(f"Total de arquivos substituídos: {replaced}")
        logger.info(f"Total de arquivos ignorados: {ignored}")
