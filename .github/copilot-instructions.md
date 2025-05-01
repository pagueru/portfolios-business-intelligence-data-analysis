# copilot-instructions.md

Projetos em Python devem seguir as Python Enhancement Proposals (PEPs), as convenções de nomenclatura e tipagem do Python, e as melhores práticas da linguagem. Além disso, as seguintes diretrizes específicas devem ser observadas ao sugerir ou gerar código:

## 1. Nomeação e documentação

* Nomeie variáveis, funções, classes e objetos similares em inglês.
* Escreva comentários de código e docstrings em português do Brasil.
* Prefira docstrings de linha única.
  * Caso não seja possível, utilize o formato de docstrings do Google.
* Todos os comentários devem ser escritos na linguagem imperativa, como: "trata", "corrige", "faz".

## 2. Tipagem

* Utilize tipagem forte nos scripts.
  * Priorize a tipagem nativa (`str`, `int`, `list`, `dict`, etc.).
  * Utilize o módulo `typing` apenas quando a tipagem nativa não for suficiente.

## 3. Validação de código e ferramentas

* Garanta que os scripts estejam em conformidade com as ferramentas de lint e análise estática:
  * `ruff`
  * `mypy`
  * `pylint`
* Antes de submeter ou aceitar sugestões de código, certifique-se de que:
  * Todas as mensagens de erro ou aviso foram resolvidas.
  * O código segue os padrões de lint, formatação e tipagem definidos por essas ferramentas.
* Sempre que houver parâmetro booleano em funções, utilize o asterisco (*) para forçar o uso nomeado desse argumento.
* Os comentários de módulo no topo dos arquivos Python devem ser docstrings de linha única, utilizando aspas triplas.

## 4. Logging

* Use o módulo `logging` para registrar mensagens do sistema.
* Sempre instancie uma variável `logger` ou utilize a variável `logger` já existente no código.
* Utilize `f-strings` para a formatação de mensagens de log, em vez de `%s`.

## 5. Estrutura de arquivos e módulos

* Ao sugerir a criação de um arquivo Python, sempre inclua:
  * Um arquivo `__init__.py` vazio no diretório do módulo, contendo apenas os comentários de cabeçalho padrão.
  * Um comentário no cabeçalho do novo arquivo com uma breve descrição sobre o módulo/arquivo.

## 6. Manipulação de caminhos

* Trabalhe com caminhos de arquivos e diretórios utilizando o módulo `pathlib`.

## 7. Commits e versionamento

* Siga o padrão de commits convencionais, utilizando os seguintes tipos:
  * `init`: inicializações importantes no projeto, como a configuração ou organização inicial da estrutura do ambiente.
  * `feat`: adições de novas funcionalidades ao projeto, como novos módulos, processos ou scripts.
  * `fix`: correções de erros ou bugs encontrados no projeto.
  * `update`: ajustes ou melhorias que não introduzem novas funcionalidades nem corrigem erros.
* Seja extremamente detalhado com as mudanças de arquivos de código e os motivos para as mudanças ao fazer um commit.

## 8. Gerenciamento de dependências

* Utilizo `poetry` para gerenciar dependências e ambientes virtuais.
* Ao sugerir a instalação de uma nova dependência, utilize o comando:  
  `poetry add <dependência>`
