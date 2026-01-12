# ArXiv Paper Collector

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Cross-platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/)

An automated Python tool that fetches the latest papers from arXiv related to electronic structure theory and artificial intelligence, filters them by keywords, and generates formatted PDF reports using LaTeX.

## Features

- **Automated Daily Collection**: Runs automatically at scheduled times
- **Keyword Filtering**: Filters papers by customizable keywords
- **LaTeX Reports**: Generates professional PDF reports
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Portable**: Self-contained with easy installation
- **Configurable**: YAML-based configuration

## Quick Start

### Prerequisites

- Python 3.8 or higher
- LaTeX (TeX Live, MiKTeX, or MacTeX)

### Installation

#### Option 1: Automated Installation (Recommended)

**Linux/macOS:**
```bash
git clone https://github.com/YOUR_USERNAME/arxiv-paper-collector.git
cd arxiv-paper-collector
chmod +x install.sh
./install.sh
```

**Windows:**
```cmd
git clone https://github.com/YOUR_USERNAME/arxiv-paper-collector.git
cd arxiv-paper-collector
install.bat
```

#### Option 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/arxiv-paper-collector.git
cd arxiv-paper-collector

# Install dependencies
pip install -r requirements.txt

# Install LaTeX (if not installed)
# macOS: brew install mactex
# Ubuntu: sudo apt-get install texlive-full
# Windows: Download from https://miktex.org/
```

## Usage

### Basic Commands

```bash
# Run once immediately
python main.py --run

# Using launcher script
./run.sh --run       # Linux/macOS
run.bat --run        # Windows

# Edit keywords
python main.py --edit-keywords

# Start scheduled daemon
python main.py --daemon

# Check status
python main.py --status
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--run, -r` | Run the paper collector once immediately |
| `--daemon, -d` | Run as a daemon with scheduled execution |
| `--config, -c` | Path to configuration file |
| `--status, -s` | Show scheduler status |
| `--edit-keywords` | Open config file in default editor |

## Configuration

### Config File Locations

The program searches for configuration files in the following order:

1. Current directory: `./config.yaml`
2. User home: `~/.arxiv-collector/config.yaml`
3. System config: `~/.config/arxiv-collector/config.yaml` (Linux/macOS)
   or `%APPDATA%\arxiv-collector\config.yaml` (Windows)

### Creating User Config

```bash
python main.py --edit-keywords
```

Or manually:
```bash
mkdir -p ~/.config/arxiv-collector
cp config.yaml ~/.config/arxiv-collector/
```

### Config File Structure

```yaml
# Keywords for filtering papers
keywords:
  electronic_structure:
    - "electronic structure"
    - "DFT"
    - "quantum chemistry"
  artificial_intelligence:
    - "machine learning"
    - "neural network"
    - "AI"

# arXiv categories to search
arxiv_categories:
  - "physics.comp-ph"
  - "cs.AI"

# Date range (days back from today)
days_back: 1

# Schedule (daily run time)
schedule:
  hour: 10
  minute: 0

# Output directories
output:
  pdf_dir: "output/papers"
  latex_dir: "output/latex"

# LaTeX settings
latex:
  engine: "xelatex"  # pdflatex, xelatex, or lualatex
```

## Project Structure

```
arxiv-paper-collector/
├── config.yaml              # Configuration file
├── main.py                  # Main entry point
├── setup.py                 # pip install setup
├── requirements.txt         # Python dependencies
├── install.sh              # Linux/macOS installer
├── install.bat             # Windows installer
├── run.sh                  # Linux/macOS launcher
├── run.bat                 # Windows launcher
├── modules/
│   ├── __init__.py
│   ├── arxiv_fetcher.py    # arXiv API integration
│   ├── paper_filter.py     # Keyword filtering
│   ├── latex_generator.py  # LaTeX document generation
│   ├── pdf_compiler.py     # PDF compilation
│   ├── scheduler.py        # Task scheduling
│   └── config_loader.py    # Configuration management
├── templates/
│   └── paper_report.tex    # LaTeX template
└── output/
    ├── papers/             # Generated PDFs
    └── latex/              # LaTeX source files
```

## System Integration

### Cron (Linux/macOS)

Edit crontab (`crontab -e`):
```bash
# Run daily at 10 AM
0 10 * * * cd /path/to/arxiv-paper-collector && python3 main.py --run >> output/cron.log 2>&1
```

### systemd (Linux)

Create `/etc/systemd/system/arxiv-collector.service`:
```ini
[Unit]
Description=ArXiv Paper Collector
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/arxiv-paper-collector
ExecStart=/usr/bin/python3 main.py --daemon
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable arxiv-collector
sudo systemctl start arxiv-collector
```

### Task Scheduler (Windows)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to Daily at 10:00 AM
4. Action: Start a program
   - Program: `python`
   - Arguments: `main.py --run`
   - Start in: `C:\path\to\arxiv-paper-collector`

## Portable Usage

### Using Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install
pip install -r requirements.txt

# Run
python main.py --run
```

### pip Installation

```bash
pip install -e .
arxiv-collector --run
```

## Troubleshooting

### LaTeX Compilation Fails

1. Ensure LaTeX is installed: `pdflatex --version`
2. Try different engine in config: `xelatex` or `lualatex`
3. Check log file: `output/collector.log`

### No Papers Found

- Increase `days_back` in config
- Check `arxiv_categories` are correct
- Verify keywords aren't too specific

### Import Errors

```bash
pip install --upgrade -r requirements.txt
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [arXiv](https://arxiv.org/) for open access to scientific papers
- [arxiv.py](https://github.com/lukasschwab/arxiv.py) for API access
- [Jinja2](https://jinja.palletsprojects.com/) for template engine
