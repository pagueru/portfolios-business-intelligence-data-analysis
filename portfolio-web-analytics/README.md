# Web Analytics: Goodreads e Kaggle num só registro

Aula prática da disciplina Web Analytics, unidade de técnicas de coleta de dados. O pipeline busca um mangá no Goodreads, extrai os dados da página, cruza com um dataset público do Kaggle e grava tudo num JSON. O caso usado é *Oyasumi Punpun*, de Inio Asano.

![Execução do pipeline no terminal](images/uv_run_main.py.gif)

Fica como caso de estudo de coleta na web: os dados raspados não vão para o repositório (veja [Dados e termos de uso](#dados-e-termos-de-uso)).

## O que o pipeline faz

1. Lê a configuração em [`src/config/files/settings.yaml`](src/config/files/settings.yaml): o título buscado, o dataset do Kaggle e o tempo de cache.
2. Busca o título no Goodreads e baixa o HTML da página do livro com `httpx`. A cópia local vale por 10 minutos, para não repetir requisições.
3. Extrai título, autor, páginas, nota, número de avaliações e biografia do autor com BeautifulSoup. Os seletores ficam em [`parser.yaml`](src/config/files/parser.yaml), fora do código.
4. Baixa o dataset [Manga and Anime Dataset](https://www.kaggle.com/datasets/duongtruongbinh/manga-and-anime-dataset) com o `kagglehub` e filtra a linha do mangá com pandas.
5. Junta as duas fontes e grava `data/output/pipeline_results.json`.

Cada etapa também roda sozinha pelos scripts de [`examples/`](examples).

## Resultado

Trecho do JSON de uma execução:

```json
{
  "goodreads": {
    "title": "Goodnight Punpun Omnibus, Vol. 1",
    "author": "Inio Asano",
    "pages": 426,
    "rating": 4.27,
    "ratings_count": 20395,
    "reviews": 1984
  },
  "kaggle": {
    "title": "Oyasumi Punpun (Goodnight Punpun)",
    "score": 9.01,
    "ranked": 10,
    "volumes": 13,
    "chapters": 147,
    "status": "Finished",
    "genres": ["Drama", "Slice of Life"],
    "demographics": ["Seinen"]
  }
}
```

As duas fontes se completam: o Goodreads traz a recepção do volume 1 em inglês, e o Kaggle traz a obra inteira (volumes, capítulos, gênero, ranking).

## Como rodar

Precisa de Python 3.13 e [uv](https://docs.astral.sh/uv/getting-started/installation/). Os comandos rodam a partir desta pasta, porque os caminhos de configuração são relativos a ela.

```bash
uv sync --all-extras
uv run main.py
```

Ou, com o `Makefile`: `make install` e `make run`. Sem uv, `pip install -r requirements.txt` e `python main.py`.

O dataset do Kaggle é público. Se o `kagglehub` pedir autenticação, configure o token como descrito na [documentação do kagglehub](https://github.com/Kaggle/kagglehub#authenticate).

O notebook [`jupyter/manga-dataset.ipynb`](jupyter/manga-dataset.ipynb) explora o dataset do Kaggle à parte.

## Dados e termos de uso

O projeto é acadêmico. O HTML do Goodreads e o CSV do Kaggle são gerados na execução e ficam fora do git: os termos do Goodreads restringem coleta automatizada, e o dataset do Kaggle reúne dados de terceiros. Quem rodar o pipeline deve respeitar os termos de cada plataforma e a LGPD.

## Estrutura

```text
portfolio-web-analytics/
├── main.py                       # monta e executa o pipeline
├── src/
│   ├── config/                   # leitura e validação do settings.yaml e do parser.yaml
│   ├── infrastructure/
│   │   ├── datasources/          # scraper e parser do Goodreads, provider do Kaggle
│   │   └── logger.py
│   ├── pipeline/                 # junta as fontes e grava o JSON
│   └── common/                   # erros, classe base e utilitários
├── examples/                     # cada etapa rodando sozinha
├── jupyter/                      # exploração do dataset do Kaggle
├── data/                         # html/, datasets/ e output/, gerados na execução
├── docs/roteiro-aula-pratica.pdf # roteiro da faculdade
└── images/                       # gif da execução
```

## Próximos passos

- Testes unitários para o parser e o provider do Kaggle.
- Uma classe própria para normalizar os dados, hoje espalhada pelo pipeline.
- Rodar para vários mangás e gravar num SQLite.
- Simplificar o `parser.yaml`, que dá trabalho para manter.
