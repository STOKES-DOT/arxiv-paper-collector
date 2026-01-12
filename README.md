# ArXiv Paper Collector

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Cross-platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

An automated Python tool that fetches the latest papers from arXiv related to electronic structure theory and artificial intelligence, filters them by keywords, and generates formatted PDF reports using LaTeX.

## Features

- **Automated Daily Collection**: Runs automatically at scheduled times
- **Keyword Filtering**: Filters papers by customizable keywords
- **LaTeX Reports**: Generates professional PDF reports with hyperlinks
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Portable**: Self-contained with auto-installation
- **Configurable**: Simple YAML-based configuration

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Quick Install](#quick-install)
  - [Manual Install](#manual-install)
  - [LaTeX Installation](#latex-installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

---

## Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.8+ | `python --version` |
| pip | Latest | `pip --version` |
| LaTeX | Any | `pdflatex --version` |

---

## Installation

### Quick Install (Recommended)

#### Linux/macOS

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/arxiv-paper-collector.git
cd arxiv-paper-collector

# 2. Run the installer
chmod +x install.sh
./install.sh

# 3. Run the program
./run.sh --run
```

#### Windows

```cmd
REM 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/arxiv-paper-collector.git
cd arxiv-paper-collector

REM 2. Run the installer
install.bat

REM 3. Run the program
run.bat --run
```

**The installer will:**
- ✓ Check Python version
- ✓ Check LaTeX installation
- ✓ Install Python dependencies
- ✓ Create output directories
- ✓ Update configuration

---

### Manual Install

If the automated installer doesn't work, follow these steps:

#### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Packages installed:**
- `arxiv` - arXiv API client
- `PyYAML` - Configuration parsing
- `Jinja2` - Template engine
- `python-dateutil` - Date handling
- `colorlog` - Colored logging
- `schedule` - Task scheduling

#### Step 2: Install LaTeX

See [LaTeX Installation](#latex-installation) below.

#### Step 3: Verify Installation

```bash
python main.py --help
```

---

### LaTeX Installation

LaTeX is **required** for PDF generation. Choose your platform:

#### macOS

```bash
# Option 1: Homebrew (smaller download)
brew install mactex-no-gui

# Option 2: Full MacTeX
brew install --cask mactex
```

**Download size:** ~100MB (no-gui) or ~4GB (full)

#### Ubuntu/Debian

```bash
# Basic LaTeX installation
sudo apt-get update
sudo apt-get install texlive-latex-extra

# Full installation (recommended)
sudo apt-get install texlive-full
```

**Download size:** ~500MB (basic) or ~4GB (full)

#### Fedora/RHEL

```bash
sudo dnf install texlive-scheme-full
```

#### Windows

**Option 1: MiKTeX (Recommended)**

1. Download from [miktex.org](https://miktex.org/download)
2. Run the installer
3. Choose "Complete" installation

**Option 2: TeX Live**

1. Download from [tug.org](https://www.tug.org/texlive/)
2. Run `install-tl-windows.bat`
3. Follow the installation wizard

#### Verify LaTeX Installation

```bash
pdflatex --version    # Should show version info
xelatex --version     # Alternative engine (better Unicode support)
```

**Troubleshooting LaTeX:**
- If LaTeX is not found after installation, **restart your terminal/command prompt**
- On Windows, MiKTeX may ask to install packages on first use - click "Yes"

---

## Usage

### Basic Commands

```bash
# Run once immediately
python main.py --run

# Using launcher scripts (recommended)
./run.sh --run       # Linux/macOS
run.bat --run        # Windows

# Edit keywords in config file
python main.py --edit-keywords

# Show next scheduled run time
python main.py --status

# Start scheduled daemon (runs daily at configured time)
python main.py --daemon
```

### Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--run` | `-r` | Run the paper collector once immediately |
| `--daemon` | `-d` | Run as a daemon with scheduled execution |
| `--config` | `-c` | Path to configuration file |
| `--status` | `-s` | Show scheduler status |
| `--edit-keywords` | | Open config file in default editor |

### First Run Example

```bash
$ ./run.sh --run

============================================================
Starting ArXiv Paper Collector
============================================================

Step 1: Fetching papers from arXiv...
Found 394 papers

Step 2: Filtering papers by keywords...
  electronic_structure: 327 papers
  artificial_intelligence: 317 papers
  uncategorized: 14 papers

Step 3: Generating LaTeX document...

Step 4: Compiling PDF...
PDF generated successfully: output/papers/arxiv_papers_2026-01-12.pdf

============================================================
Collection completed successfully!
============================================================
```

---

## Configuration

### Config File Locations

The program searches for configuration files in this order:

1. **Current directory**: `./config.yaml`
2. **User home**: `~/.arxiv-collector/config.yaml`
3. **System config**:
   - Linux/macOS: `~/.config/arxiv-collector/config.yaml`
   - Windows: `%APPDATA%\arxiv-collector\config.yaml`

### Creating a User Config

**Method 1: Using the editor**
```bash
python main.py --edit-keywords
```

**Method 2: Manual creation**
```bash
# Create config directory
mkdir -p ~/.config/arxiv-collector

# Copy default config
cp config.yaml ~/.config/arxiv-collector/

# Edit the file
nano ~/.config/arxiv-collector/config.yaml
```

### Config File Explained

```yaml
# ============================================
# KEYWORDS - Papers matching these will be collected
# ============================================
keywords:
  electronic_structure:
    - "electronic structure"
    - "density functional theory"
    - "DFT"
    - "quantum chemistry"
    - "ab initio"
    - "first-principles"
    - "Hartree-Fock"
    - "post-Hartree-Fock"
    - "coupled cluster"

  artificial_intelligence:
    - "machine learning"
    - "neural network"
    - "deep learning"
    - "artificial intelligence"
    - "AI"
    - "graph neural network"
    - "GNN"
    - "transformer"
    - "reinforcement learning"

# ============================================
# ARXIV CATEGORIES - Which categories to search
# ============================================
arxiv_categories:
  - "physics.comp-ph"      # Computational Physics
  - "physics.chem-ph"      # Chemical Physics
  - "cond-mat.str-el"      # Strongly Correlated Electrons
  - "cond-mat.mtrl-sci"    # Materials Science
  - "cs.LG"                # Machine Learning
  - "cs.AI"                # Artificial Intelligence

# ============================================
# TIME SETTINGS
# ============================================
days_back: 1                # How many days back to search (1=yesterday, 7=last week)
schedule:
  hour: 10                  # Run at 10:00 AM
  minute: 0
  timezone: "Asia/Shanghai" # Your timezone

# ============================================
# OUTPUT SETTINGS
# ============================================
output:
  pdf_dir: "output/papers"      # Where to save PDFs
  latex_dir: "output/latex"     # Where to save .tex files
  filename_format: "arxiv_papers_{date}.pdf"

# ============================================
# LATEX SETTINGS
# ============================================
latex:
  engine: "xelatex"        # Engine: pdflatex, xelatex, lualatex
                           # Use xelatex for better Unicode support
  max_compile_time: 60     # Max seconds to wait for compilation
  attempts: 2              # Number of compilation attempts

# ============================================
# PAPER LIMITS
# ============================================
max_papers: 50             # Maximum papers per group in report
abstract_max_length: 1000  # Maximum abstract length in characters

# ============================================
# LOGGING
# ============================================
logging:
  level: "INFO"            # DEBUG, INFO, WARNING, ERROR
  log_file: "output/collector.log"
  console_output: true
```

### Common arXiv Categories

| Category | Description |
|----------|-------------|
| `physics.comp-ph` | Computational Physics |
| `physics.chem-ph` | Chemical Physics |
| `cond-mat.str-el` | Strongly Correlated Electrons |
| `cond-mat.mtrl-sci` | Materials Science |
| `cs.LG` | Machine Learning |
| `cs.AI` | Artificial Intelligence |
| `cs.CV` | Computer Vision |
| `cs.CL` | Computation and Language |
| `stat.ML` | Machine Learning (Statistics) |

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'arxiv'"

**Solution:**
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install arxiv PyYAML Jinja2 python-dateutil colorlog schedule
```

---

### Problem: "pdflatex: command not found"

**Solution:** LaTeX is not installed or not in PATH.

**macOS:**
```bash
brew install mactex-no-gui
# Restart terminal after installation
```

**Ubuntu:**
```bash
sudo apt-get install texlive-latex-extra
```

**Windows:** Run the MiKTeX installer again and choose "Add/Remove" → "Add MiKTeX to PATH"

---

### Problem: "LaTeX Error: Unicode character not supported"

**Solution:** Change the LaTeX engine to `xelatex` in `config.yaml`:

```yaml
latex:
  engine: "xelatex"  # Changed from "pdflatex"
```

---

### Problem: "No papers found"

**Possible causes:**
1. `days_back` is too small
2. `arxiv_categories` don't have new papers
3. Keywords are too specific

**Solutions:**
```yaml
# Increase days_back
days_back: 7  # Search last 7 days instead of 1

# Add more categories
arxiv_categories:
  - "cs.AI"
  - "cs.LG"
  - "physics.comp-ph"
  - "physics.chem-ph"

# Use broader keywords
keywords:
  my_group:
    - "learning"      # Broader than "machine learning"
    - "network"       # Broader than "neural network"
```

---

### Problem: PDF compilation fails with "! Emergency stop"

**Causes:** LaTeX syntax error in generated template

**Solutions:**
1. Check the log file: `output/collector.log`
2. Try a different LaTeX engine: `xelatex` or `lualatex`
3. Reduce `max_papers` to limit report size
4. Reduce `abstract_max_length` to avoid long abstracts

---

### Problem: "Permission denied" when running scripts

**Linux/macOS:**
```bash
chmod +x install.sh run.sh
```

---

### Problem: Virtual environment issues

**Recreate virtual environment:**
```bash
# Remove old venv
rm -rf venv

# Create new one
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall
pip install -r requirements.txt
```

---

## Examples

### Example 1: Collect papers for specific topic

Edit `config.yaml`:
```yaml
keywords:
  my_research:
    - "quantum computing"
    - "qubit"
    - "entanglement"

arxiv_categories:
  - "quant-ph"
```

Run:
```bash
python main.py --run
```

---

### Example 2: Scheduled daily collection

**Using cron (Linux/macOS):**
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 10 AM
0 10 * * * cd /path/to/arxiv-paper-collector && python3 main.py --run >> output/cron.log 2>&1
```

**Using systemd (Linux):**
```bash
# Create service file
sudo nano /etc/systemd/system/arxiv-collector.service
```

Add:
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

---

### Example 3: Using with virtual environment

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install
pip install -r requirements.txt

# Run
python main.py --run
```

---

## System Integration

### Windows Task Scheduler

1. Open Task Scheduler (`taskschd.msc`)
2. Click "Create Basic Task"
3. Name: "ArXiv Paper Collector"
4. Trigger: "Daily" at "10:00 AM"
5. Action: "Start a program"
   - **Program**: `python`
   - **Arguments**: `main.py --run`
   - **Start in**: `C:\path\to\arxiv-paper-collector`

### LaunchAgents (macOS)

Create `~/Library/LaunchAgents/com.arxiv.collector.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.arxiv.collector</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/arxiv-paper-collector/main.py</string>
        <string>--run</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

Load:
```bash
launchctl load ~/Library/LaunchAgents/com.arxiv.collector.plist
```

---

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Format code
black .

# Run tests
pytest
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see LICENSE file for details.

---

## Acknowledgments

- [arXiv](https://arxiv.org/) for open access to scientific papers
- [arxiv.py](https://github.com/lukasschwab/arxiv.py) for Python API access
- [Jinja2](https://jinja.palletsprojects.com/) for the template engine
