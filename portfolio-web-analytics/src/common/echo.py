"""Módulo para saída no terminal personalizada."""

import re
import sys

# Constantes para formatação de texto (compatíveis com o formato do Makefile)
_RESET = "\033[0m"
_BOLD = "\033[1m"
_BLUE = "\033[34m"
_RED = "\033[31m"
_YELLOW = "\033[33m"
_GREEN = "\033[32m"
_CYAN = "\033[36m"
_MAGENTA = "\033[35m"

# Símbolos para os tipos de mensagem
_INFO_SYMBOL = f"{_BOLD}{_BLUE}i{_RESET}"
_ERROR_SYMBOL = f"{_BOLD}{_RED}✖{_RESET}"
_WARN_SYMBOL = f"{_BOLD}{_YELLOW}!{_RESET}"
_SUCCESS_SYMBOL = f"{_BOLD}{_GREEN}✔{_RESET}"
_WAIT_SYMBOL = f"{_BOLD}{_CYAN}…{_RESET}"
_ARROW_SYMBOL = f"{_BOLD}{_BLUE}➔{_RESET}"
_BULLET_SYMBOL = f"{_BOLD}{_CYAN}•{_RESET}"
_STAR_SYMBOL = f"{_BOLD}{_YELLOW}★{_RESET}"
_PROGRESS_SYMBOL = f"{_BOLD}{_CYAN}>{_RESET}"
_TIME_SYMBOL = f"{_BOLD}{_BLUE}⧗{_RESET}"
_FLAG_SYMBOL = f"{_BOLD}{_RED}⚑{_RESET}"
_LINK_SYMBOL = f"{_BOLD}{_CYAN}⧉{_RESET}"

# Mapeamento de tipos de mensagem para símbolos
_SYMBOL_MAP = {
    "info": _INFO_SYMBOL,
    "error": _ERROR_SYMBOL,
    "warn": _WARN_SYMBOL,
    "success": _SUCCESS_SYMBOL,
    "wait": _WAIT_SYMBOL,
    "arrow": _ARROW_SYMBOL,
    "bullet": _BULLET_SYMBOL,
    "star": _STAR_SYMBOL,
    "progress": _PROGRESS_SYMBOL,
    "time": _TIME_SYMBOL,
    "flag": _FLAG_SYMBOL,
    "link": _LINK_SYMBOL,
}


def echo(message: str, message_type: str = "info") -> str | None:
    """Formata e imprime mensagem no estilo do Makefile."""
    if message_type == "blank":
        formatted_message = message
    else:
        symbol = _SYMBOL_MAP.get(message_type.lower(), _INFO_SYMBOL)
        formatted_message = f"{symbol} {message}"

    # Verifica se estamos em ambiente de terminal que suporta cores
    if hasattr(sys, "stdout") and hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        print(formatted_message)
    else:
        # Remove códigos ANSI se não for terminal
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        print(ansi_escape.sub("", formatted_message))


if __name__ == "__main__":
    echo("info", "info")
    echo("error", "error")
    echo("warn", "warn")
    echo("success", "success")
    echo("wait", "wait")
    echo("arrow", "arrow")
    echo("bullet", "bullet")
    echo("star", "star")
    echo("progress", "progress")
    echo("time", "time")
    echo("flag", "flag")
    echo("link", "link")
    echo("blank", "blank")
