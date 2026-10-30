.PHONY: help show.status.icons install clean.venv start start.docker remove.docker open.mongo-express lint
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

start: ## Abre o menu que extrai as consultas e gera o PDF do relatório
	@echo -e "$(INFO) Iniciando aplicação..."
	@uv run python main.py

start.docker: ## Sobe o MongoDB e o mongo-express em segundo plano
	@echo -e "$(INFO) Inicializando docker compose em segundo plano..."
	@docker compose up -d

remove.docker: ## Remove os containers e os volumes
	@echo -e "$(INFO) Removendo containers..."
	@docker compose down -v

open.mongo-express: ## Abre o mongo-express no navegador
	@echo -e "$(INFO) Abrindo o mongo-express no navegador..."
	@start http://localhost:8081 || open http://localhost:8081

lint: ## Corrige o lint e formata o código com o ruff
	@echo -e "$(INFO) Corrigindo lint e formatação..."
	@uv run ruff check .; uv run ruff format . && uv run ruff check .
