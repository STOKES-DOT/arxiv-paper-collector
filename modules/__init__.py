"""
Arxiv Paper Collector - Modules Package
"""

__version__ = "1.0.0"
__author__ = "Jiaoyuan"

from .arxiv_fetcher import ArxivFetcher
from .paper_filter import PaperFilter
from .latex_generator import LatexGenerator
from .pdf_compiler import PdfCompiler
from .scheduler import PaperScheduler
from .notifications import NotificationManager, send_test_notification
from .config_loader import ConfigLoader

__all__ = [
    "ArxivFetcher",
    "PaperFilter",
    "LatexGenerator",
    "PdfCompiler",
    "PaperScheduler",
    "NotificationManager",
    "send_test_notification",
    "ConfigLoader",
]
