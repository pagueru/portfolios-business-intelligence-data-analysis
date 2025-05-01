"""Script para extrair codeblocks do arquivo notes.md e gerar arquivos na pasta querys."""

import logging
from pathlib import Path
import re


def print_terminal_line(value: int = 80, char: str = "-") -> None:
    """Imprime uma linha no terminal com o caractere especificado."""
    if value <= 0:
        msg = "O valor deve ser maior que 0."
        raise ValueError(msg)
    print(char * value)


def start_config(*, clear_terminal: bool = True) -> None:
    """Limpa o terminal e marca o início do script."""
    if clear_terminal:
        print("\033[H\033[J", end="", flush=True)
    print_terminal_line()


def setup_logger() -> logging.Logger:
    """Configura e retorna o logger do sistema."""
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def read_codeblocks(md_path: Path) -> list[tuple[str, str]]:
    """Lê o arquivo markdown e retorna uma lista de tuplas (nome, código)."""
    content = md_path.read_text(encoding="utf-8")
    pattern = re.compile(r"```js\s*//\s*(\S+)\s*\n(.*?)```", re.DOTALL)
    return pattern.findall(content)


def confirm_run(total: int) -> bool:
    """Pergunta ao usuário se deseja prosseguir com a criação dos arquivos."""
    resposta = input(
        f"➔ Deseja gerar arquivos para os {total} codeblocks encontrados? (1 = sim, 0 = não): "
    )
    return resposta.strip() == "1"


def check_existing_files(matches: list[tuple[str, str]], output_dir: Path) -> set[str]:
    """Verifica quais arquivos já existem na pasta de saída."""
    existing = set()
    for name, _ in matches:
        filename = name.strip()
        if not filename.endswith(".js"):
            filename = f"{filename}.js"
        file_path = output_dir / filename
        if file_path.exists():
            existing.add(filename)
    return existing


def confirm_overwrite(existing_count: int) -> bool:
    """Pergunta ao usuário se deseja substituir arquivos existentes."""
    resposta = input(
        f"➔ {existing_count} arquivos já existem. Deseja substituir? (1 = sim, 0 = não): "
    )
    return resposta.strip() == "1"


def save_codeblocks(
    matches: list[tuple[str, str]],
    output_dir: Path,
    logger: logging.Logger,
    *,
    overwrite: bool = False,
) -> tuple[int, int, int]:
    """Salva os codeblocks extraídos, controlando criação, substituição e ignorados."""
    created = 0
    replaced = 0
    ignored = 0
    for name, code in matches:
        filename = name.strip()
        if not filename.endswith(".js"):
            filename = f"{filename}.js"
        file_path = output_dir / filename
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


def main() -> None:
    """Executa o fluxo principal do script."""
    start_config()
    logger = setup_logger()
    md_path = Path("./docs/notes.md")
    output_dir = Path("./querys")
    if not md_path.exists():
        logger.error(f"Arquivo {md_path} não encontrado.")
        return
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
        logger.info(f"Diretório {output_dir} criado.")
    logger.info("Iniciando extração de codeblocks do arquivo Markdown.")
    matches = read_codeblocks(md_path)
    total_files = len(matches)
    logger.info(f"Foram encontrados {total_files} codeblocks para extração.")
    if not matches:
        logger.warning("Nenhum codeblock encontrado.")
        return
    if not confirm_run(total_files):
        logger.info("Execução abortada pelo usuário.")
        return
    existing = check_existing_files(matches, output_dir)
    overwrite = True
    if existing:
        logger.info(f"{len(existing)} arquivos já existem na pasta de saída.")
        overwrite = confirm_overwrite(len(existing))
        if not overwrite:
            logger.info("Arquivos existentes serão ignorados.")
    created, replaced, ignored = save_codeblocks(
        matches=matches, output_dir=output_dir, logger=logger, overwrite=overwrite
    )
    logger.info(f"Total de arquivos criados: {created}")
    logger.info(f"Total de arquivos substituídos: {replaced}")
    logger.info(f"Total de arquivos ignorados: {ignored}")


if __name__ == "__main__":
    main()
