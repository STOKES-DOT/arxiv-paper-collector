#!/usr/bin/env python3
"""
ArXiv Paper Collector - Main Entry Point
Automatically fetches, filters, and generates PDF reports for arXiv papers
"""

import argparse
import logging
import sys
import os
from datetime import datetime
from pathlib import Path
import yaml

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules import (
    ArxivFetcher,
    PaperFilter,
    LatexGenerator,
    PdfCompiler,
    PaperScheduler
)


def setup_logging(config: dict) -> logging.Logger:
    """
    Setup logging configuration

    Args:
        config: Configuration dictionary

    Returns:
        Configured logger
    """
    log_config = config.get("logging", {})
    log_level = getattr(logging, log_config.get("level", "INFO"))
    log_file = log_config.get("log_file", "output/collector.log")
    console_output = log_config.get("console_output", True)

    # Create logger
    logger = logging.getLogger("ArXivCollector")
    logger.setLevel(log_level)

    # Remove existing handlers
    logger.handlers = []

    # Create formatters
    try:
        from colorlog import ColoredFormatter
        console_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    except ImportError:
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # File handler
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load configuration from YAML file

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: Config file not found: {config_path}. Using defaults.")
        return get_default_config()
    except Exception as e:
        print(f"Error loading config: {e}. Using defaults.")
        return get_default_config()


def get_default_config() -> dict:
    """Get default configuration"""
    return {
        "keywords": {
            "electronic_structure": ["electronic structure", "DFT", "quantum chemistry"],
            "artificial_intelligence": ["machine learning", "neural network", "AI"]
        },
        "arxiv_categories": ["physics.comp-ph", "physics.chem-ph", "cs.LG"],
        "days_back": 1,
        "schedule": {"hour": 10, "minute": 0},
        "output": {
            "pdf_dir": "output/papers",
            "latex_dir": "output/latex"
        },
        "latex": {
            "engine": "pdflatex",
            "max_compile_time": 60,
            "attempts": 2
        },
        "max_papers": 50,
        "abstract_max_length": 1000,
        "logging": {
            "level": "INFO",
            "log_file": "output/collector.log",
            "console_output": True
        }
    }


def run_collector(config: dict, logger: logging.Logger) -> bool:
    """
    Run the paper collection pipeline

    Args:
        config: Configuration dictionary
        logger: Logger instance

    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting ArXiv Paper Collector")
        logger.info("=" * 60)

        # Initialize components
        output_config = config.get("output", {})
        pdf_dir = output_config.get("pdf_dir", "output/papers")
        latex_dir = output_config.get("latex_dir", "output/latex")

        os.makedirs(pdf_dir, exist_ok=True)
        os.makedirs(latex_dir, exist_ok=True)

        # Step 1: Fetch papers from arXiv
        logger.info("Step 1: Fetching papers from arXiv...")
        fetcher = ArxivFetcher(
            categories=config.get("arxiv_categories", []),
            days_back=config.get("days_back", 1),
            max_results=100
        )
        papers = fetcher.fetch_papers()

        if not papers:
            logger.warning("No papers found. Exiting.")
            return False

        logger.info(f"Found {len(papers)} papers")

        # Step 2: Filter papers by keywords
        logger.info("Step 2: Filtering papers by keywords...")
        filter_config = config.get("keywords", {})
        paper_filter = PaperFilter(keywords=filter_config)
        grouped_papers = paper_filter.filter_papers(papers)

        for group_name, group_papers in grouped_papers.items():
            logger.info(f"  {group_name}: {len(group_papers)} papers")

        # Step 3: Generate LaTeX document
        logger.info("Step 3: Generating LaTeX document...")
        latex_gen = LatexGenerator()

        date_str = datetime.now().strftime("%Y-%m-%d")
        latex_filename = f"arxiv_papers_{date_str}.tex"
        latex_path = os.path.join(latex_dir, latex_filename)

        latex_gen.generate_latex(
            papers=grouped_papers,
            output_path=latex_path,
            max_papers=config.get("max_papers", 50),
            abstract_max_length=config.get("abstract_max_length", 1000)
        )

        # Step 4: Compile PDF
        logger.info("Step 4: Compiling PDF...")
        latex_config = config.get("latex", {})
        compiler = PdfCompiler(
            engine=latex_config.get("engine", "pdflatex"),
            max_compile_time=latex_config.get("max_compile_time", 60),
            attempts=latex_config.get("attempts", 2)
        )

        pdf_path = compiler.compile(latex_path, output_dir=pdf_dir)

        if pdf_path:
            logger.info(f"PDF generated successfully: {pdf_path}")
            logger.info("=" * 60)
            logger.info("Collection completed successfully!")
            logger.info("=" * 60)
            return True
        else:
            logger.error("PDF compilation failed")
            return False

    except Exception as e:
        logger.error(f"Error during collection: {e}", exc_info=True)
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="ArXiv Paper Collector - Automated paper collection and PDF generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run once immediately
  python main.py --run

  # Run with custom config
  python main.py --run --config my_config.yaml

  # Start scheduled daemon (runs daily at 10 AM)
  python main.py --daemon

  # Show next scheduled run time
  python main.py --status
        """
    )

    parser.add_argument(
        "--run", "-r",
        action="store_true",
        help="Run the paper collector once immediately"
    )

    parser.add_argument(
        "--daemon", "-d",
        action="store_true",
        help="Run as a daemon with scheduled execution"
    )

    parser.add_argument(
        "--config", "-c",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )

    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show scheduler status and next run time"
    )

    parser.add_argument(
        "--edit-keywords",
        action="store_true",
        help="Open config file in default editor for keyword editing"
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)
    logger = setup_logging(config)

    # Handle --edit-keywords
    if args.edit_keywords:
        editor = os.environ.get('EDITOR', 'nano')
        logger.info(f"Opening {args.config} in {editor}...")
        os.system(f"{editor} {args.config}")
        return

    # Handle --status
    if args.status:
        schedule_config = config.get("schedule", {})
        hour = schedule_config.get("hour", 10)
        minute = schedule_config.get("minute", 0)
        print(f"Next scheduled run: {hour:02d}:{minute:02d} daily")
        return

    # Handle --run
    if args.run:
        success = run_collector(config, logger)
        sys.exit(0 if success else 1)

    # Handle --daemon
    if args.daemon:
        logger.info("Starting daemon mode...")
        schedule_config = config.get("schedule", {})
        scheduler = PaperScheduler(
            hour=schedule_config.get("hour", 10),
            minute=schedule_config.get("minute", 0)
        )

        # Schedule daily task
        scheduler.schedule_daily(lambda: run_collector(config, logger))

        # Start scheduler
        scheduler.start()
        logger.info(f"Scheduler running. Next run at {schedule_config.get('hour', 10):02d}:{schedule_config.get('minute', 0):02d}")
        logger.info("Press Ctrl+C to stop...")

        try:
            while True:
                import time
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            scheduler.stop()
            sys.exit(0)

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
