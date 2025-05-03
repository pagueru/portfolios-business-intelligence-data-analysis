"""Configura e fornece instância de logger para o projeto."""

import logging

if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )
logging.getLogger("weasyprint").setLevel(logging.ERROR)


def get_logger(name: str) -> logging.Logger:
    """Retorna instância de logger configurado."""
    return logging.getLogger(name)
