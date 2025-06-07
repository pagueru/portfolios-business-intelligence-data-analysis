"""Este módulo define exceções personalizadas para o projeto."""


class ProjectError(Exception):
    """Exceção base para erros do projeto."""


class GoodreadsHTMLParserError(ProjectError):
    """Exceção para erros relacionados ao parsing de HTML do Goodreads."""


class GoodreadsScraperError(ProjectError):
    """Exceção para erros relacionados ao scraping do Goodreads."""


class KaggleDatasetProviderError(ProjectError):
    """Exceção para erros relacionados ao download de datasets do Kaggle."""


class LoggerError(ProjectError):
    """Exceção para erros relacionados à configuração do logger."""


class SettingsManagerError(ProjectError):
    """Exceção para erros relacionados à classe SettingsManager."""
