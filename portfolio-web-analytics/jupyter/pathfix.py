"""Corrige o caminho do projeto ao executar exemplos, ajustando `sys.path` dinamicamente."""

from pathlib import Path
import sys

project_path = str(Path(__file__).resolve().parent.parent)
sys.path.append(project_path)

if __name__ == "__main__":
    print(project_path)
