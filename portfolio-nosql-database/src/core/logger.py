"""Configura e fornece instância de logger para o projeto."""

import logging

if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )
logging.getLogger("weasyprint").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
