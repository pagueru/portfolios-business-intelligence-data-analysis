"""Repositories para acesso a diferentes fontes de dados."""

from repositories.goodreads import GoodreadsHTMLParser
from repositories.html_downloader import HTMLDownloader
from repositories.kaggle_downloader import KaggleDatasetDownloader

__all__ = [
    "GoodreadsHTMLParser",
    "HTMLDownloader",
    "KaggleDatasetDownloader",
]
