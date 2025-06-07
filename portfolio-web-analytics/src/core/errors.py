"""Este módulo define exceções personalizadas para o projeto."""


class ProjectError(Exception):
    """Exceção base para erros do projeto."""


class HTMLParserError(ProjectError):
    """Exceção para erros de parsing da classe GoodreadsHTMLParser."""


class HTMLDownloaderError(ProjectError):
    """Exceção genérica para erros relacionados à classe HTMLDownloader."""


class KaggleDatasetError(ProjectError):
    """Exceção para erros relacionados ao download ou análise de datasets do Kaggle."""


class LoggerError(ProjectError):
    """Exceção para erros relacionados à configuração do logger."""


class ConfigRepositoryError(ProjectError):
    """Exceção para erros relacionados à classe ConfigRepository."""
