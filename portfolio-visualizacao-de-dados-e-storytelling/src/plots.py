from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import plotly.express as px
from scipy import stats

OUTPUTS = Path(__file__).parent.parent / "outputs"
OUTPUTS.mkdir(exist_ok=True)

DPI = 120
FIG_W = 10
FIG_H = 5


def _salvar(fig, nome: str) -> Path:
    caminho = OUTPUTS / nome
    fig.savefig(caminho, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    return caminho


def linha_anual(df) -> Path:
    anual = df.groupby("ano").agg(
        consumo_total=("consumo_kwh", "sum"),
        valor_medio=("valor_fatura", "mean"),
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(FIG_W, FIG_H))
    cor_consumo = "#1f77b4"
    cor_valor = "#d62728"

    ax1.bar(anual["ano"], anual["consumo_total"] / 1000, color=cor_consumo,
            alpha=0.7, label="Consumo total (MWh)")
    ax1.set_xlabel("Ano", fontsize=11)
    ax1.set_ylabel("Consumo total (MWh)", color=cor_consumo, fontsize=11)
    ax1.tick_params(axis="y", labelcolor=cor_consumo)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    ax2 = ax1.twinx()
    ax2.plot(anual["ano"], anual["valor_medio"], color=cor_valor, marker="o",
             linewidth=2, label="Valor médio da fatura (R$)")
    ax2.set_ylabel("Valor médio da fatura (R$)", color=cor_valor, fontsize=11)
    ax2.tick_params(axis="y", labelcolor=cor_valor)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))

    linhas1, labels1 = ax1.get_legend_handles_labels()
    linhas2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(linhas1 + linhas2, labels1 + labels2, loc="upper right")

    plt.title("Consumo Total Anual e Valor Médio da Fatura — Palácio do Jaburu", fontsize=13)
    fig.tight_layout()
    return _salvar(fig, "fig_linha_anual.png")


def barras_mensal(df) -> Path:
    NOMES_MESES = [
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez",
    ]
    mensal = df.groupby("mes_num")["consumo_kwh"].mean().reset_index()
    mensal = mensal.sort_values("mes_num")

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    cores = ["#d62728" if m in [9, 10, 11] else "#1f77b4" for m in mensal["mes_num"]]
    ax.bar(mensal["mes_num"], mensal["consumo_kwh"] / 1000, color=cores)
    ax.set_xticks(mensal["mes_num"])
    ax.set_xticklabels([NOMES_MESES[m - 1] for m in mensal["mes_num"]])
    ax.set_xlabel("Mês", fontsize=11)
    ax.set_ylabel("Consumo médio (MWh)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.set_title("Consumo Médio Mensal (2017–2024) — barras vermelhas = pico sazonal", fontsize=12)
    fig.tight_layout()
    return _salvar(fig, "fig_barras_mensal.png")


def correlacao(df) -> Path:
    slope, intercept, r, _, _ = stats.linregress(df["consumo_kwh"], df["valor_fatura"])
    x_line = np.linspace(df["consumo_kwh"].min(), df["consumo_kwh"].max(), 200)
    y_line = slope * x_line + intercept

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    sc = ax.scatter(df["consumo_kwh"] / 1000, df["valor_fatura"],
                    c=df["ano"], cmap="viridis", alpha=0.75, s=60)
    ax.plot(x_line / 1000, y_line, color="#d62728", linewidth=2, label=f"Regressão linear")
    plt.colorbar(sc, ax=ax, label="Ano")
    ax.set_xlabel("Consumo (MWh)", fontsize=11)
    ax.set_ylabel("Valor da fatura (R$)", fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))
    ax.set_title(f"Correlação Consumo × Valor da Fatura  |  r de Pearson = {r:.3f}", fontsize=12)
    ax.legend()
    fig.tight_layout()
    return _salvar(fig, "fig_correlacao.png")


def interativo_plotly(df) -> tuple[Path, Path]:
    df_plot = df.copy()
    df_plot["mes_ano"] = df_plot["data"].dt.strftime("%b/%Y")
    df_plot["consumo_mwh"] = (df_plot["consumo_kwh"] / 1000).round(1)
    df_plot["valor_fmt"] = df_plot["valor_fatura"].apply(lambda v: f"R$ {v:,.2f}")

    fig = px.line(
        df_plot,
        x="mes_num",
        y="consumo_mwh",
        color="ano",
        markers=True,
        labels={"mes_num": "Mês", "consumo_mwh": "Consumo (MWh)", "ano": "Ano"},
        title="Consumo Mensal por Ano — Palácio do Jaburu (interativo)",
        hover_data={"mes_ano": True, "valor_fmt": True, "consumo_mwh": ":.1f"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"],
    )
    fig.update_layout(
        legend_title_text="Ano",
        hovermode="x unified",
        template="plotly_white",
    )

    html_path = OUTPUTS / "fig_interativo.html"
    fig.write_html(str(html_path))

    png_path = OUTPUTS / "fig_interativo_preview.png"
    fig.write_image(str(png_path), width=1200, height=550, scale=1.5)

    return html_path, png_path
