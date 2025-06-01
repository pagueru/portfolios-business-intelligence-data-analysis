"""Módulo de definição de tipos personalizados."""
# ruff: noqa: PLR0913, PLR0903
# pylint: disable=too-many-arguments, too-many-positional-arguments

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

type PathLike = str | Path
"""Tipo que representa um caminho, podendo ser uma string ou um objeto Path."""

type PathLikeAndList = PathLike | list[PathLike]
"""Tipo que representa um caminho ou uma lista de caminhos (strings ou objetos Path)."""

type LoggerDict = dict[str, dict[str, dict[str, bool | str] | dict[str, str]]]
"""Tipo que representa um dicionário de configuração para o logger."""

type ParserDict = dict[str, dict[str, dict[str, str] | None]]
"""Tipo que representa um dicionário de configuração para o parser."""
