"""Este módulo define exceções personalizadas para o projeto."""


class ProjectError(Exception):
    """Exceção base para erros do projeto."""


class HTMLParserError(Exception):
    """Exceção para erros de parsing da classe GoodreadsHTMLParser."""


class HTMLDownloaderError(Exception):
    """Exceção genérica para erros relacionados à classe HTMLDownloader."""


class KaggleDatasetError(Exception):
    """Exceção para erros relacionados ao download ou análise de datasets do Kaggle."""


class ProjectUtilsError(Exception):
    """Exceção para erros relacionados à classe ProjectUtils."""


class LoggerError(Exception):
    """Exceção para erros relacionados à configuração do logger."""
