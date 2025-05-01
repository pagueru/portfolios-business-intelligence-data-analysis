# Roteiro de Aula Prática - Bancos de Dados Não Relacionais

## NOME DA DISCIPLINA: Bancos de Dados Não Relacionais [cite: 2]

## OBJETIVOS

* Criar e manipular um banco de dados não relacional no MongoDB[cite: 3].

## INFRAESTRUTURA

### Instalações [cite: 4]

* Laboratório de Informática [cite: 4]

### Materiais de consumo [cite: 4]

* **Descrição:** Computador [cite: 4]
* **Quantidade:** 01 por aluno [cite: 4]

### Software [cite: 4]

* **Sim (X)** Não () [cite: 4]
* **Pago () Não Pago (X)** [cite: 5]
* **Tipo de Licença:** Freeware [cite: 5]
* **Descrição do software:**
  * **MongoDB Community Server:** Banco de dados orientado a documentos, livre, de código aberto e multiplataforma [C++](cite: 5). Classificado como NoSQL[cite: 6]. Download: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community) [cite: 7]
  * **MongoDB Compass:** Ferramenta gráfica interativa para consultar, otimizar e analisar dados do MongoDB[cite: 7]. Instalado opcionalmente com o MongoDB Server[cite: 8].

### Equipamento de Proteção Individual (EPI) [cite: 9]

* NSA [cite: 9]

## PROCEDIMENTOS PRÁTICOS

### Procedimento/Atividade № 1 [cite: 9]

* **Atividade proposta:** Criar um banco de dados no MongoDB Compass, inserir e atualizar documentos em uma collection[cite: 9].
* **Procedimentos:**
  * Criar banco de dados "lojadb" no MongoDB Compass[cite: 10].
  * **Etapa 1:**
    * Criar a collection "vendas"[cite: 12].
    * Inserir dados básicos dos clientes [usar comando "insert" na Shell ou Compass](cite: 13, 14).
      * **Nota:** O campo telefone deve ser uma Array[cite: 15]. Bancos não relacionais não exigem estrutura fixa [ex: Marcos sem email, quantidades diferentes de telefones](cite: 17).
      * **Dados:**

                | NOME   | CLIENTE VIP (1-SIM/0-NÃO) | EMAIL           | TELEFONE                        |
                | :----- | :------------------------ | :-------------- | :------------------------------ |
                | João   | 1                         | <joao@email.com>  | 9999-1111, 8888-1111            |
                | Marcos | 0                         |                 | 9999-2222                       |
                | Maria  | 1                         | <maria@email.com> | 9999-3333, 8888-3333, 9988-3000 |
                [cite: 16]

  * **Etapa 2:**
    * Atualizar documentos existentes na collection "vendas"[cite: 18].
    * Adicionar endereço como campo do tipo Objeto [rua, número, complemento, cidade, estado](cite: 19, 20).
      * **Dados:**

                | NOME   | ENDEREÇO                                   |
                | :----- | :----------------------------------------- |
                | João   | Rua Um, 1000, Apto 1 Bloco 1. São Paulo/SP |
                | Marcos | Rua Dois, 4000. Campinas/SP                |
                | Maria  | Rua Três, 3000. Londrina/PR              |
                [cite: 21]

    * Adicionar dados das compras (no mesmo documento do cliente) usando Arrays de Objetos no campo "compras"[cite: 22, 23, 24].
      * **Dados:**

                | NOME   | COMPRAS                                                                                                                                |
                | :----- | :------------------------------------------------------------------------------------------------------------------------------------- |
                | João   | Nome do produto: notebook<br>Preço: R$ 5000,00<br>Quantidade: 1                                                                          |
                | Marcos | Nome do produto: Caderno<br>Preço: R$ 20,00<br>Quantidade: 1<br>Nome do produto: Caneta<br>Preço: R$ 3,00<br>Quantidade: 5                   |
                | Maria  | Nome do produto: Borracha<br>Preço: R$ 2,00<br>Quantidade: 2<br>Nome do produto: Tablet<br>Preço: R$ 2500,00<br>Quantidade: 1<br>Nome do produto: Capa para tablet<br>Preço: R$ 50,00<br>Quantidade: 1 |
                [cite: 25, 27]

### Procedimento/Atividade № 2 [cite: 28]

* **Atividade proposta:** Realizar pesquisas e consultas em um banco de dados não relacional [MongoDB](cite: 28).
* **Contexto:** Utilizar o banco "lojadb" e a collection "vendas" criados anteriormente[cite: 29].
* **Instruções:** Informar o comando correto para cada consulta[cite: 30].
  * **DICA:** Usar `.pretty()` no final do comando de busca via linha de comando para identar o resultado[cite: 30].
* **Consultas:**
    1. Retornar todos os documentos da collection[cite: 31].
    2. Localizar as informações da cliente "Maria"[cite: 31].
    3. Retornar os clientes VIPs (VIP=1), exibindo apenas o campo "nome"[cite: 32].
    4. Exibir as compras efetuadas por "Marcos"[cite: 33].
    5. Retornar todos os nomes de produtos comprados por todos os clientes [usar linha de comando MongoDB](cite: 33, 34).

### Checklist [cite: 35]

* [ ] Acessar o MongoDB Compass
* [ ] Criar um banco de dados no MongoDB
* [ ] Criar uma collection em um banco de dados
* [ ] Inserir documentos na collection criada
* [ ] Atualizar a collection "vendas" no banco de dados "lojadb" conforme tabelas
* [ ] Navegar até a collection "vendas" do banco de dados "lojadb" [cite: 36]
* [ ] Realizar as 5 consultas especificadas [cite: 36]

## RESULTADOS [cite: 37]

* Espera-se que o aluno saiba desenvolver bancos de dados não relacionais orientados a documentos no MongoDB, incluindo criação de collections, inserção/atualização de documentos e realização de consultas[cite: 37].
