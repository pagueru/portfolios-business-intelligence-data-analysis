.PHONY: install install-dev
include config.mk

help: ## Mostra esta ajuda.
	@echo -e "$(BOLD)Monorepo:$(RESET)"
	@echo -e "  $(BOLD)$(CYAN)$(MONOREPO_NAME)$(RESET)"
	@echo -e ""
	@echo -e "$(BOLD)Repo:$(RESET)"
	@echo -e "  $(BOLD)$(CYAN)$(APP_NAME)$(RESET)"
	@echo -e ""
	@echo -e "$(BOLD)Uso:$(RESET)"
	@echo -e "  make [alvo]"
	@echo -e ""
	@echo -e "$(BOLD)Opções disponíveis:$(RESET)"
	@grep -E '^[a-zA-Z0-9_.-]+:.*## ' $(firstword $(MAKEFILE_LIST)) | \
	sed -e 's/\\$$//' -e 's/##//' | \
	awk -F ': ' '{ printf "  $(CYAN)%-20s$(RESET) %s\n", $$1, $$2 }'
	@echo -e ""
	@echo -e "Para mais informações, veja: $(CYAN)https://github.com/pagueru/$(MONOREPO_NAME)$(RESET)"

show.status.icons: ## Exibe os ícones de status e seus significados
	@echo -e "$(SUCCESS) Sucesso: Operação concluída com êxito."
	@echo -e "$(ERROR) Erro: Algo deu errado."
	@echo -e "$(INFO) Informação: Mensagem informativa."
	@echo -e "$(WARN) Aviso: Atenção necessária."
	@echo -e "$(WAIT) Aguardando: Processo em andamento."
	@echo -e "$(TITLE) Título: Cabeçalho ou destaque."
	@echo -e "$(LINE) Linha: Separador visual."
	@echo -e "$(TAB) Tabulação: Espaçamento ou indentação."

install: ## Instala as dependências do projeto
	@echo -e "$(INFO) Instalando dependências..."
	@uv sync --all-extras

clean.venv: ## Remove o ambiente virtual do projeto
	@echo -e "$(INFO) Removendo ambiente virtual..."
	@if [ -d ".venv" ]; then \
		rm -rf .venv; \
	else \
		echo -e "$(WARN) .venv já removido"; \
	fi

run: ## Inicializa a aplicação em produção
	@echo -e "$(INFO) Iniciando aplicação..."
	@uv run main.py

start.docker: ## Inicializa o docker-compose em segundo plano
	@echo -e "$(INFO) Inicializando docker-compose em segundo plano..."
	@docker-compose up -d

remove.docker: ## Remove o docker-compose e os containers
	@echo -e "$(INFO) Removendo docker-compose e containers..."
	@docker-compose down -v

open.dbeaver: ## Abre o host do DBeaver no navegador
	@echo -e "$(INFO) Abrindo o host do DBeaver no navegador..."
	@start http://localhost:8978/#/ || open http://localhost:8978/#/

test.all: ## Executa todos os testes com pytest
	@echo -e "$(INFO) Executando testes..."
	@if [ -d "tests" ]; then \
		poetry run pytest; \
	else \
		echo -e "$(WARN) Diretório de testes não encontrado"; \
	fi

test.debug: ## Executa os testes e imprime os logs
	@echo -e "$(INFO) Executando testes com logs..."
	@if [ -d "tests" ]; then \
		poetry run pytest -s; \
	else \
		echo -e "$(WARN) Diretório de testes não encontrado"; \
	fi

test.cobertura: ## Executa análise de cobertura do projeto
	@echo -e "$(INFO) Executando análise de cobertura..."
	@if [ -d "tests" ]; then \
		poetry run pytest tests --cov=src; \
	else \
		echo -e "$(WARN) Diretório de testes não encontrado"; \
	fi

test.cobertura.html: ## Executa análise de cobertura e gera relatório em HTML.
	@echo -e "$(INFO) Gerando relatório de cobertura em HTML..."
	@if [ -d "tests" ]; then \
		poetry run pytest tests --cov=src --cov-report=html; \
	else \
		echo -e "$(WARN) Diretório de testes não encontrado"; \
	fi

test.ruff: ## Verifica a formatação do código
	@echo -e "$(INFO) Verificando formatação do código..."
	@if [ -d "src" ]; then \
		poetry run ruff check . --fix; \
	else \
		echo -e "$(WARN) Diretório de código-fonte não encontrado"; \
	fi

test.pre-commit: ## Executa o pre-commit para verificar o código
	@echo -e "$(INFO) Executando pre-commit..."
	@if [ -d ".git" ]; then \
		pre-commit run --all-files; \
	else \
		echo -e "$(WARN) Diretório .git não encontrado"; \
	fi

corrigir.docs: ## Corrige a formatação do código
	ruff --select D205 --fix .
