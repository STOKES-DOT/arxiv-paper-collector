"""
Configuration Loader Module
Handles loading configuration from multiple locations with portability support
"""

import os
import yaml
from pathlib import Path
from typing import Optional, Dict
import logging


class ConfigLoader:
    """Load configuration from multiple locations with fallback support"""

    # Config file locations in order of priority
    CONFIG_LOCATIONS = [
        # Current directory
        "{cwd}/config.yaml",
        # User home directory
        "{home}/.arxiv-collector/config.yaml",
        # User config directory (platform-specific)
        "{config_dir}/arxiv-collector/config.yaml",
    ]

    @staticmethod
    def get_config_dir() -> str:
        """Get platform-specific config directory"""
        system = os.name
        home = Path.home()

        if system == 'nt':  # Windows
            config_dir = os.environ.get('APPDATA', home / 'AppData' / 'Roaming')
        elif system == 'posix':  # Linux/macOS
            config_dir = os.environ.get('XDG_CONFIG_HOME', home / '.config')
        else:
            config_dir = str(home)

        return str(config_dir)

    @classmethod
    def find_config_file(cls, config_path: Optional[str] = None) -> Optional[str]:
        """
        Find configuration file from multiple locations

        Args:
            config_path: Explicit config file path (highest priority)

        Returns:
            Path to config file, or None if not found
        """
        # If explicit path provided, try it first
        if config_path:
            if os.path.exists(config_path):
                return config_path
            print(f"Warning: Config file not found: {config_path}")

        # Try standard locations
        cwd = os.getcwd()
        home = str(Path.home())
        config_dir = cls.get_config_dir()

        for location_template in cls.CONFIG_LOCATIONS:
            location = location_template.format(cwd=cwd, home=home, config_dir=config_dir)
            if os.path.exists(location):
                return location

        return None

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> Dict:
        """
        Load configuration from file with fallback to defaults

        Args:
            config_path: Optional explicit config file path

        Returns:
            Configuration dictionary
        """
        config_file = cls.find_config_file(config_path)

        if config_file:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                logging.info(f"Loaded config from: {config_file}")
                return config
            except Exception as e:
                logging.warning(f"Error loading config from {config_file}: {e}")

        # Return default config
        logging.info("Using default configuration")
        return cls.get_default_config()

    @staticmethod
    def get_default_config() -> Dict:
        """Get default configuration"""
        return {
            "keywords": {
                "electronic_structure": [
                    "electronic structure", "DFT", "quantum chemistry",
                    "ab initio", "first-principles"
                ],
                "artificial_intelligence": [
                    "machine learning", "neural network", "AI",
                    "deep learning", "transformer"
                ]
            },
            "arxiv_categories": [
                "physics.comp-ph", "physics.chem-ph", "cs.LG", "cs.AI"
            ],
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

    @classmethod
    def create_user_config(cls) -> str:
        """
        Create user config directory and default config file

        Returns:
            Path to created config file
        """
        config_dir = os.path.join(cls.get_config_dir(), "arxiv-collector")
        os.makedirs(config_dir, exist_ok=True)

        config_file = os.path.join(config_dir, "config.yaml")

        if not os.path.exists(config_file):
            default_config = cls.get_default_config()
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)

            print(f"Created config file: {config_file}")

        return config_file

    @classmethod
    def get_output_paths(cls, config: Dict) -> Dict[str, str]:
        """
        Resolve output paths, expanding user home directory

        Args:
            config: Configuration dictionary

        Returns:
            Dictionary with resolved output paths
        """
        output_config = config.get("output", {})

        paths = {
            "pdf_dir": cls._expand_path(output_config.get("pdf_dir", "output/papers")),
            "latex_dir": cls._expand_path(output_config.get("latex_dir", "output/latex")),
            "log_file": cls._expand_path(config.get("logging", {}).get("log_file", "output/collector.log"))
        }

        return paths

    @staticmethod
    def _expand_path(path: str) -> str:
        """
        Expand user home directory in path

        Args:
            path: Path string, may contain ~

        Returns:
            Expanded absolute path
        """
        expanded = os.path.expanduser(path)
        if not os.path.isabs(expanded):
            expanded = os.path.abspath(expanded)
        return expanded
