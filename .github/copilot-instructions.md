# copilot-instructions.md

Projetos em Python devem seguir as Python Enhancement Proposals (PEPs), as convenções de nomenclatura e tipagem do Python, e as melhores práticas da linguagem. Além disso, as seguintes diretrizes específicas devem ser observadas ao sugerir ou gerar código:

## Diretrizes de Código e Estruturação de Projetos

### Nomeação, Documentação e Tipagem

* Nomeie variáveis, funções, classes e objetos similares em inglês.
* Escreva comentários de código e docstrings em português do Brasil, preferencialmente de linha única (ou formato Google se necessário), sempre na linguagem imperativa (ex: "trata", "corrige").
* Utilize tipagem forte, priorizando tipos nativos (`str`, `int`, `list`, `dict`, etc.); use o módulo `typing` apenas quando necessário.

### Validação, Logging e Estrutura

* Garanta conformidade com `ruff`, `mypy` e `pylint`, resolvendo todos os avisos antes de submeter código.
* Parâmetros booleanos em funções devem ser nomeados via asterisco (*).
* Comentários de módulo no topo dos arquivos Python devem ser docstrings de linha única.
* Use o módulo `logging` com a variável `logger` e `f-strings` para logs.
* Estruture arquivos com `__init__.py` vazio e cabeçalho descritivo.
* Utilize `pathlib` para manipulação de arquivos e diretórios.

### Commits e Dependências

* Escreva commits em português do Brasil.
* Siga o padrão de commits convencionais: `init`, `feat`, `fix`, `update`, detalhando mudanças e motivos.
* Use `poetry` para dependências e ambientes virtuais (`poetry add <dependência>`).

---

## Diretrizes de Uso de Ferramentas e Fluxo de Trabalho

* Utilize todas as ferramentas disponíveis (Sequential Thinking, Brave Search, Puppeteer, Knowledge Graph) conforme necessário, sem exigir ativação explícita.
* Inicie cada nova conversa com Sequential Thinking para definir as ferramentas necessárias.

### Fluxo de Trabalho Principal

1. **Análise Inicial (Sequential Thinking):**
   * Divida a consulta em componentes principais, conceitos e relações-chave.
   * Planeje a estratégia de pesquisa e verificação, definindo as ferramentas para cada etapa.
   * Exemplo: "Quais etapas são necessárias para responder à pergunta? Quais ferramentas usar em cada uma?"

2. **Pesquisa e Verificação (Brave Search & Puppeteer):**
   * Realize pesquisas amplas e direcionadas, controlando volume (count, offset) e documentando consultas, URLs, títulos, datas e descrições.
   * Navegue em sites relevantes, tire capturas de tela (sempre com URL e data/hora), extraia dados, explore links e registre caminhos de interação.
   * Repita etapas de verificação se necessário.
   * Exemplo de citação: "Título da página", URL, data de acesso: DD/MM/AAAA.

3. **Processamento e Armazenamento (Knowledge Graph):**
   * Analise/processo dados coletados, crie visualizações se útil e armazene descobertas importantes no Knowledge Graph, mantendo links e contexto das fontes.

4. **Síntese e Apresentação:**
   * Estruture e combine informações de todas as ferramentas, apresente resultados de forma clara, destaque insights e gere artifacts (código, visualizações, documentos) conforme necessário.

### Documentação e Rastreabilidade

* Todas as fontes devem ser citadas com URLs completas, títulos, datas e metadados.
* Capturas de tela devem conter URL de origem e carimbo de data/hora.
* Descobertas devem ser rastreáveis até as fontes originais.
* O Knowledge Graph deve manter links/contexto das fontes para reutilização futura.

---

## Diretrizes Específicas de Ferramentas

### Brave Search

* Controle volume de resultados (count, offset), documente consultas/resultados, rastreie caminhos e preserve metadados.

### Puppeteer

* Tire capturas de tela de evidências importantes (com URL/data/hora), use seletores precisos e documente caminhos. Repita tentativas em caso de erro.

### Sequential Thinking

* Divida tarefas complexas em etapas gerenciáveis, documente o processo de pensamento e permita revisões/ramificações.

---

## Notas de Implementação

* Use ferramentas proativamente e, quando apropriado, em paralelo.
* Documente cada etapa da análise.
* Tarefas complexas devem acionar o fluxo de trabalho completo.
* Gerencie a retenção de conhecimento entre conversas via Knowledge Graph.

---

### Exemplos Práticos

* **Citação de fonte:**
  * "Como usar o pathlib em Python", <https://docs.python.org/3/library/pathlib.html>, acesso em 02/05/2025.
* **Docstring de função:**
  * `"""Retorna o caminho absoluto do arquivo."""`
* **Sequential Thinking:**
  * 1. Identificar objetivo → 2. Listar etapas → 3. Definir ferramenta para cada etapa → 4. Executar e revisar.
