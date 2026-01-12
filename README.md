# ArXiv Paper Collector

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated Python tool that fetches the latest papers from arXiv related to electronic structure theory and artificial intelligence, filters them by keywords, and generates formatted PDF reports using LaTeX.

## Features

- **Automated Daily Collection**: Runs automatically at 10:00 AM every day
- **Keyword Filtering**: Filters papers by customizable keywords (electronic structure, AI/ML)
- **LaTeX Reports**: Generates professional PDF reports with paper summaries
- **Configurable**: Easy YAML-based configuration for keywords and settings
- **Portable**: Self-contained Python package with minimal dependencies

## Project Structure

```
arxiv-paper-collector/
├── config.yaml                 # Configuration file (edit keywords here)
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── modules/
│   ├── __init__.py
│   ├── arxiv_fetcher.py        # arXiv API integration
│   ├── paper_filter.py         # Keyword filtering
│   ├── latex_generator.py      # LaTeX document generation
│   ├── pdf_compiler.py         # PDF compilation
│   └── scheduler.py            # Task scheduling
├── templates/
│   └── paper_report.tex        # LaTeX template
└── output/
    ├── papers/                 # Generated PDFs
    ├── latex/                  # Intermediate LaTeX files
    └── collector.log           # Log file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Git (for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/arxiv-paper-collector.git
cd arxiv-paper-collector
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Verify LaTeX Installation

```bash
pdflatex --version
```

If LaTeX is not installed, install it:
- **macOS**: `brew install mactex`
- **Ubuntu/Debian**: `sudo apt-get install texlive-full`
- **Windows**: Download and install [MiKTeX](https://miktex.org/)

## Usage

### Quick Start

Run the collector once immediately:

```bash
python main.py --run
```

### Edit Keywords

To customize the keywords used for filtering papers:

```bash
python main.py --edit-keywords
```

Or edit `config.yaml` directly:

```yaml
keywords:
  electronic_structure:
    - "electronic structure"
    - "density functional theory"
    - "DFT"
    - "quantum chemistry"
    # Add your keywords here...

  artificial_intelligence:
    - "machine learning"
    - "neural network"
    - "deep learning"
    # Add your keywords here...
```

### Scheduled Execution

Run as a daemon (starts scheduler):

```bash
python main.py --daemon
```

The daemon will run the collector daily at the time specified in `config.yaml` (default: 10:00 AM).

### Check Status

```bash
python main.py --status
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--run, -r` | Run the paper collector once immediately |
| `--daemon, -d` | Run as a daemon with scheduled execution |
| `--config, -c` | Path to configuration file (default: config.yaml) |
| `--status, -s` | Show scheduler status |
| `--edit-keywords` | Open config file in default editor |

## Configuration

The `config.yaml` file contains all settings:

### Keywords

Define keyword groups for filtering papers:

```yaml
keywords:
  electronic_structure:
    - "electronic structure"
    - "DFT"
  artificial_intelligence:
    - "machine learning"
    - "AI"
```

### arXiv Categories

Specify which arXiv categories to search:

```yaml
arxiv_categories:
  - "physics.comp-ph"      # Computational Physics
  - "physics.chem-ph"      # Chemical Physics
  - "cs.LG"                # Machine Learning
```

### Schedule

Set the daily run time:

```yaml
schedule:
  hour: 10
  minute: 0
  timezone: "Asia/Shanghai"
```

### Output

Configure output directories:

```yaml
output:
  pdf_dir: "output/papers"
  latex_dir: "output/latex"
```

### LaTeX Compilation

Configure LaTeX engine:

```yaml
latex:
  engine: "pdflatex"       # Options: pdflatex, xelatex, lualatex
  max_compile_time: 60
  attempts: 2
```

## System Integration

### Cron (Linux/macOS)

Add to crontab (`crontab -e`):

```bash
0 10 * * * cd /path/to/arxiv-paper-collector && /usr/bin/python3 main.py --run >> output/cron.log 2>&1
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

Enable and start:

```bash
sudo systemctl enable arxiv-collector
sudo systemctl start arxiv-collector
```

## Output

The tool generates:

1. **PDF Report**: `output/papers/arxiv_papers_YYYY-MM-DD.pdf`
   - Grouped by keyword categories
   - Contains title, authors, abstract, and arXiv links

2. **LaTeX Source**: `output/latex/arxiv_papers_YYYY-MM-DD.tex`
   - Can be customized or compiled manually

3. **Log File**: `output/collector.log`
   - Detailed run information for debugging

## Dependencies

- `arxiv` - arXiv API client
- `PyYAML` - Configuration file parsing
- `Jinja2` - LaTeX template engine
- `python-dateutil` - Date handling

## Troubleshooting

### LaTeX Compilation Fails

- Ensure LaTeX is installed: `pdflatex --version`
- Check log file: `output/collector.log`
- Try different engine in config (xelatex, lualatex)

### No Papers Found

- Check `days_back` setting in config
- Verify arXiv categories are correct
- Check keywords are not too specific

### Permission Errors

- Ensure output directories are writable
- Check file permissions: `chmod +x main.py`

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details

## Author

Jiaoyuan

## Acknowledgments

- [arXiv](https://arxiv.org/) for open access to scientific papers
- [arxiv Python library](https://github.com/lukasschwab/arxiv.py) for API access
