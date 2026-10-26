# Portfolio: Visualização de Dados e Storytelling

Atividade da disciplina de Visualização de Dados e Storytelling: contar, com gráficos, a história do consumo de energia elétrica do Palácio do Jaburu entre junho de 2017 e setembro de 2024. O resultado é um relatório em `.docx` e `.pdf`, montado por script a partir dos dados.

![Consumo anual](outputs/fig_linha_anual.png)

## Dados

Consumo mensal em kWh e valor bruto da fatura, do CSV disponibilizado no material da disciplina. O script baixa o CSV da URL que está em `src/load_data.py`; a pasta `data/` é cache local e fica fora do git.

## Gráficos

| Arquivo | O que mostra |
| --- | --- |
| `outputs/fig_linha_anual.png` | Consumo total por ano (MWh) e valor médio da fatura, em dois eixos |
| `outputs/fig_barras_mensal.png` | Consumo médio por mês do ano, com o pico sazonal destacado |
| `outputs/fig_correlacao.png` | Dispersão entre consumo e valor da fatura, com o r de Pearson |
| `outputs/fig_interativo_preview.png` | Prévia do gráfico interativo em Plotly do consumo mensal por ano; o `.html` é gerado pelo script e fica fora do git |

## Como gerar

```bash
pip install -r requirements.txt
python src/build_docx.py
```

O script baixa os dados, gera os gráficos em `outputs/`, calcula a correlação e monta o relatório `.docx`. O `.pdf` em `outputs/` é a versão entregue.

## Estrutura

```text
src/
  load_data.py   # download e limpeza do CSV (mês por extenso, valor em reais)
  plots.py       # os quatro gráficos (matplotlib e Plotly)
  build_docx.py  # monta o relatório com python-docx
outputs/         # gráficos e relatório entregue
```
