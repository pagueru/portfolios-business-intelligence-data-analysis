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

clear.venv: ## Remove o ambiente virtual do projeto
	@echo -e "$(INFO) Removendo ambiente virtual..."
	@if [ -d ".venv" ]; then \
		rm -rf .venv; \
	else \
		echo -e "$(WARN) .venv já removido"; \
	fi

run: ## Inicializa a aplicação em produção
	@echo -e "$(INFO) Iniciando aplicação..."
	@uv run main.py

requirements: 
	@echo -e "$(INFO) Gerando requirements.txt..."
	@uv export --no-hashes --no-header --format requirements-txt > requirements.txt