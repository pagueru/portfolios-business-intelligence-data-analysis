import re
from pathlib import Path

import pandas as pd
import requests

CSV_URL = (
    "https://raw.githubusercontent.com/AndersonSalata/Materiais_Alunos_EAD"
    "/main/consumo-de-energia-eletrica-no-palacio-do-jaburu-2017-2024-setembro.csv"
)

MESES = {
    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
    "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
    "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
}

DATA_DIR = Path(__file__).parent.parent / "data"


def _baixar_csv() -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    destino = DATA_DIR / "jaburu.csv"
    if not destino.exists():
        r = requests.get(CSV_URL, timeout=30)
        r.raise_for_status()
        destino.write_bytes(r.content)
    return destino


def _parse_valor(texto: str) -> float:
    limpo = re.sub(r"[R$\s]", "", str(texto))
    limpo = limpo.replace(".", "").replace(",", ".")
    return float(limpo)


def carregar() -> pd.DataFrame:
    caminho = _baixar_csv()
    df = pd.read_csv(caminho, sep=";", encoding="latin-1")
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={
        "ano": "ano",
        "mês": "mes_nome",
        "mes": "mes_nome",
        "consumo-kwh": "consumo_kwh",
        " valor bruto da fatura ": "valor_fatura",
        "valor bruto da fatura": "valor_fatura",
    })
    # normaliza nomes de coluna com espaços residuais
    df.columns = [c.strip() for c in df.columns]

    df["mes_num"] = df["mes_nome"].str.lower().str.strip().map(MESES)
    df["valor_fatura"] = df["valor_fatura"].apply(_parse_valor)
    df["consumo_kwh"] = pd.to_numeric(df["consumo_kwh"], errors="coerce")
    df["data"] = pd.to_datetime(
        df["ano"].astype(str) + df["mes_num"].astype(str).str.zfill(2),
        format="%Y%m",
    )
    df = df.sort_values("data").reset_index(drop=True)
    return df
