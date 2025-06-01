# copilot-instructions.md

## Diretrizes de Uso de Ferramentas e Fluxo de Trabalho

* Utilize todas as ferramentas disponíveis (Sequential Thinking, Brave Search, Knowledge Graph) conforme necessário, sem exigir ativação explícita.
* Inicie cada nova conversa com Sequential Thinking (`#sequentialthinking`) para definir as ferramentas necessárias.

### Fluxo de Trabalho Principal

1. **Análise Inicial (Sequential Thinking):**
    * Divida tarefas complexas (com múltiplos passos, dependências ou que exijam pesquisa externa) em etapas gerenciáveis, documente o processo de pensamento e permita revisões/ramificações.
    * Divida a consulta em componentes principais, conceitos e relações-chave.
    * Planeje a estratégia de pesquisa e verificação, definindo as ferramentas para cada etapa.
    * **Exemplo:** Para criar uma função que lê um arquivo CSV e retorna um dicionário:
        1. **Identificar objetivo:** Criar função `ler_csv_para_dict`.
        2. **Listar etapas:**
            * Pesquisar como ler arquivos CSV em Python. (Brave Search)
            * Pesquisar como criar dicionários em Python. (Brave Search)
            * Definir a estrutura do dicionário de saída.
            * Implementar a função.
            * Testar a função com um arquivo CSV de exemplo.
        3. **Definir ferramenta para cada etapa:** Brave Search para pesquisa, Python para implementação e teste.
        4. **Executar e revisar:** Implementar, testar e ajustar o código conforme necessário.

2. **Pesquisa e Verificação (Brave Search):**
    * Realize pesquisas amplas e direcionadas, controlando volume (count, offset) e documentando consultas, URLs, títulos, datas e descrições.
    * Navegue em sites relevantes, tire capturas de tela (sempre com URL e data/hora), extraia dados, explore links e registre caminhos de interação.
    * Repita etapas de verificação se necessário.
    * **Exemplo de citação:** "Como usar o pathlib em Python", <https://docs.python.org/3/library/pathlib.html>, acesso em 02/05/2025.

3. **Processamento e Armazenamento (Knowledge Graph):**
    * Analise e processe os dados coletados, crie visualizações se útil e armazene descobertas importantes no Knowledge Graph, mantendo links e contexto das fontes para reutilização futura. **O Knowledge Graph é crucial para reter aprendizados e acelerar futuras análises.**
    * Siga estes passos para cada interação:
        1. **Identificação do Usuário:**
            * Considere que está interagindo com default_user.
            * Caso ainda não tenha identificado default_user, tente fazê-lo proativamente.
        2. **Recuperação de Memória:**
            * Sempre inicie o chat dizendo apenas "Lembrando..." e recupere todas as informações relevantes da sua memória (Knowledge Graph).
            * Sempre se refira ao Knowledge Graph como sua "memória".
        3. **Memória:**
            * Durante a conversa, esteja atento a qualquer nova informação que se enquadre nas seguintes categorias:
                a) Identidade básica (idade, gênero, localização, cargo, nível educacional, etc.)
                b) Comportamentos (interesses, hábitos, etc.)
                c) Preferências (estilo de comunicação, idioma preferido, etc.)
                d) Objetivos (metas, aspirações, etc.)
                e) Relacionamentos (relações pessoais e profissionais até 3 graus de separação)
        4. **Atualização de Memória:**
            * Se alguma nova informação for obtida durante a interação, atualize sua memória da seguinte forma:
                a) Crie entidades para organizações recorrentes, pessoas e eventos significativos.
                b) Conecte-as às entidades atuais usando relações.
                c) Armazene fatos sobre elas como observações.

4. **Síntese e Apresentação:**
    * Estruture e combine informações de todas as ferramentas, apresente resultados de forma clara, destaque insights e gere artefatos (código, visualizações, documentos) conforme necessário.

### Documentação e Rastreabilidade

* Todas as fontes devem ser citadas com URLs completas, títulos, datas e metadados (evite repetir esta orientação em outras seções).
* Capturas de tela devem conter URL de origem e carimbo de data/hora.
* Descobertas devem ser rastreáveis até as fontes originais.
* O Knowledge Graph deve manter links e contexto das fontes para reutilização futura.
* Documente cada etapa da análise em comentários ou docstrings, conforme apropriado.
* Use ferramentas proativamente e, quando apropriado, em paralelo (não repita esta orientação em outras seções). **Por exemplo, iniciar uma pesquisa com Brave Search enquanto analisa dados previamente armazenados no Knowledge Graph.**
* Tarefas complexas são aquelas que envolvem múltiplos passos, dependências externas ou pesquisa; acione o fluxo de trabalho completo nesses casos.
* Gerencie a retenção de conhecimento entre conversas via Knowledge Graph.

---

## Diretrizes de Código e Estruturação de Projetos

Projetos em Python devem seguir as Python Enhancement Proposals (PEPs), as convenções de nomenclatura e tipagem do Python, e as melhores práticas da linguagem.

### Nomeação, Documentação e Tipagem

* Nomeie variáveis, funções, classes e objetos similares em inglês.
* Escreva comentários de código e docstrings em português do Brasil, preferencialmente de linha única (ou formato Google se necessário), sempre na linguagem imperativa (ex: "trate", "corrige").
* Utilize tipagem forte, priorizando tipos nativos (`str`, `int`, `list`, `dict`, etc.); use o módulo `typing` apenas quando necessário.

### Validação, Logging e Estrutura

* Garanta conformidade com `ruff`, `mypy` e `pylint`, resolvendo todos os avisos antes de submeter código.
* Parâmetros booleanos em funções devem ser keyword-only (usando `*` na assinatura da função).
* Comentários de módulo no topo dos arquivos Python devem ser docstrings de linha única.
* Majoritariamente utilizee f-strings para formatação de strings.
* Use o módulo `logging` com a variável `logger` f-strings para logs.
* Estruture arquivos com `__init__.py` vazio e cabeçalho descritivo (docstring de linha única no topo).
* Utilize `pathlib` para manipulação de arquivos e diretórios.
* A docstring do método `__init__` deve seguir o padrão: `"""Inicializa a classe."""`
* Ao implementar alterações em código ou sugestões, preserve sempre todos os comentários e marcações TODO existentes.
* Sempre que lançar exceção com raise, utilize o método `logger.exception` para registrar a exceção.

### Commits e Dependências

* Escreva commits em português do Brasil.
* Siga o [padrão de commits convencionais](https://www.conventionalcommits.org/pt-br/v1.0.0/): `init`, `feat` (nova funcionalidade), `fix` (correção de bug), `update` (atualização), detalhando as mudanças e os motivos. **Exemplos:** `feat: adiciona autenticação de usuário`, `fix: corrige erro de cálculo no relatório`.
* Use `uv` para dependências e ambientes virtuais (`uv add <dependência>`).

---

### Exemplos Práticos

* **Citação de fonte:**
  * "Como usar o pathlib em Python", <https://docs.python.org/3/library/pathlib.html>, acesso em 02/05/2025.
* **Docstring de função:**
  * """Retorne o caminho absoluto do arquivo."""
* **Sequential Thinking:**
  * 1. Identificar objetivo → 2. Listar etapas → 3. Definir ferramenta para cada etapa → 4. Executar e revisar.
* **Utilizacao de blocos `try...except`:**
    1. Caso esteja usando a função `echo`, utilize:
        ```python	
        except <ExceptionName> as exc:
            echo(f"<mensagem_de_erro>: {exc}", "error")
            raise
        ```
    2. Caso esteja usando o `logger`, utilize:
        ```python	
        except <ExceptionName>:
            logger.exception("<mensagem_de_erro>.")
            raise
        ```