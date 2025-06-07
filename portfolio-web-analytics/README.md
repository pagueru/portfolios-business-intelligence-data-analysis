# Pipeline de Web Analytics — Projeto Acadêmico e Profissional

Este projeto implementa um pipeline automatizado de web analytics para extração, transformação e análise de dados de mangás, integrando scraping do Goodreads, parsing HTML parametrizado por YAML e análise de datasets do Kaggle.

O pipeline na estrutura atual foi testado apenas com o mangá Oyasumi Punpun, ainda sendo necessário aplicar mudanças conforme mencionado no [Melhorias e Tarefas Futuras](#melhorias-e-tarefas-futuras). Outras obras podem exigir ajustes no parser ou configurações.

Este projeto evolui iniciativas anteriores de webscraping, como o [py-selenium-scraper](https://github.com/pagueru/py-selenium-scraper), adotando princípios de Clean Architecture para aprendizado.

> [!IMPORTANT]  
> **Atenção ética:** Este projeto é destinado a fins acadêmicos e demonstração técnica. Ao utilizar técnicas de scraping e análise de dados, é fundamental respeitar os termos de uso das plataformas, a legislação vigente (LGPD, GDPR etc.) e os princípios éticos de privacidade e consentimento. Sempre reflita sobre o impacto social, a finalidade e a responsabilidade no uso e compartilhamento de dados coletados.

## Fluxo do Pipeline

O pipeline é composto por etapas bem definidas, cada uma orquestrada por uma classe principal do projeto:

1. **Leitura das configurações** (`ConfigRepository`)
   * Carrega e valida os arquivos de configuração YAML (`settings.yaml` e `parser.yaml`).
   * Garante que todos os parâmetros necessários estejam presentes para o funcionamento do pipeline.

2. **Scraping do Goodreads** (`GoodreadsRepository`)
   * Realiza a busca do livro/mangá no site Goodreads, utilizando os parâmetros definidos em `settings.yaml`.
   * Faz o download do HTML da página do livro e salva em disco, utilizando cache para evitar downloads desnecessários.

3. **Parsing do HTML** (`ParserRepository`)
   * Utiliza o HTML baixado e o arquivo `parser.yaml` para extrair informações estruturadas (título, autor, páginas, avaliações, etc.).
   * Normaliza e formata os dados extraídos para uso posterior.

4. **Download e filtragem do dataset Kaggle** (`KaggleRepository`)
   * Baixa o dataset de mangás do Kaggle, conforme especificado em `settings.yaml`.
   * Filtra o dataset para obter apenas os dados do mangá de interesse.
   * Converte os dados filtrados para JSON.

5. **Normalização e união dos dados** (`WebAnalyticsPipeline`)
   * Realiza a normalização final dos dados extraídos do Goodreads e Kaggle.
   * Une os dados em um único dicionário estruturado.

6. **Exportação do JSON final**
   * Salva o resultado consolidado em `data/output/pipeline_results.json`.

7. **Exibição dos resultados no terminal**
   * Mostra no terminal, de forma formatada, os dados tratados de Goodreads e Kaggle para fácil conferência.

## Instalação e Requisitos

* Python 3.10+ (recomendado 3.13)
* [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências

Instalação recomendada (usando uv):

```bash
uv sync --all-extras
```

Alternativamente, você pode instalar as dependências via `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Configuração dos Arquivos YAML

### settings.yaml

```yaml
# Exemplo de configuração
# Caminho: src/config/settings.yaml
goodreads:
  book_url_base: "https://www.goodreads.com/book/show/"
  search_url_base: "https://www.goodreads.com/search?query="
  search_book_title: "PunPun"
  cache_seconds: 600
  book_fallback: "25986929-goodnight-punpun-omnibus-vol-1"

kaggle:
  manga_name: "PunPun"
  dataset_name: "duongtruongbinh/manga-and-anime-dataset"
  dataset_files:
    - "manga.csv"
  force_download: false
```

## Execução do Pipeline

```bash
uv run main.py
```

## Exemplo de Saída — Resultado Final

### Exemplo de JSON Final

```json
{
  "goodreads": {
    "title": "Goodnight Punpun Omnibus, Vol. 1",
    "author": "Inio Asano",
    "pages": 426,
    "publication": "First published January 1, 2006",
    "ratings_count": 20394,
    "reviews": 1984,
    "rating": 4.27,
    "author_books": 106,
    "author_followers": 2,
    "author_bio": "Inio Asano ( 浅野いにお , Asano Inio ) is a Japanese cartoonist. ...",
    "description": "Meet Punpun Punyama. He’s an average kid in an average town..."
  },
  "kaggle": {
    "title": "Oyasumi Punpun (Goodnight Punpun)",
    "score": 9.01,
    "vote": 176269,
    "ranked": 10,
    "popularity": 9,
    "members": 430160,
    "favorite": 51039,
    "volumes": 13,
    "chapters": 147,
    "status": "Finished",
    "published": "Mar  15, 2007 to Nov  2, 2013",
    "genres": ["Drama", "Slice of Life"],
    "themes": [],
    "demographics": ["Seinen"],
    "serialization": "Big Comic Spirits",
    "author": "Asano, Inio (Story & Art)"
  }
}
```

## Melhorias e Tarefas Futuras

* [ ] Melhorar o tratamento de erros e mensagens para o usuário
* [ ] Separar uma classe dedicada para o tratamento e normalização dos dados
* [ ] Validar múltiplos mangás e alimentar um banco SQLite
* [ ] Simplificar o parse do HTML (o uso do YAML é interessante, mas a manutenção do arquivo é trabalhosa)
* [ ] Corrigir redundância de variáveis, utilizando constantes globais
* [ ] Remover `lint.ignore` temporários do `pyproject.toml` e corrigir os erros apontados pelo linter
* [ ] Atualizar os comandos do Makefile para facilitar a automação

## Contato

GitHub: [pagueru](https://github.com/pagueru/)

LinkedIn: [Raphael Coelho](https://www.linkedin.com/in/raphaelhvcoelho/)

E-mail: [raphael.phael@gmail.com](mailto:raphael.phael@gmail.com)
