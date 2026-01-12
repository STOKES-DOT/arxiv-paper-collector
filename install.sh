#!/bin/bash
# ArXiv Paper Collector - Installation Script
# Supports Linux and macOS

set -e

echo "=================================="
echo "ArXiv Paper Collector Installer"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_CMD=python3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found, attempting to install..."
    python3 -m ensurepip --upgrade
fi

# Check LaTeX installation
echo ""
echo "Checking LaTeX installation..."
if command -v pdflatex &> /dev/null; then
    echo "✓ LaTeX (pdflatex) found"
    LATEX_ENGINE=pdflatex
elif command -v xelatex &> /dev/null; then
    echo "✓ LaTeX (xelatex) found"
    LATEX_ENGINE=xelatex
else
    echo "⚠ LaTeX not found!"
    echo ""
    echo "LaTeX is required for PDF generation."
    echo "Please install LaTeX:"
    echo "  - macOS:     brew install mactex"
    echo "  - Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  - Fedora/RHEL:   sudo dnf install texlive-scheme-full"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    LATEX_ENGINE=pdflatex
fi

# Create virtual environment (optional)
echo ""
read -p "Create virtual environment? (recommended) [Y/n] " -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    USE_VENV=false
else
    USE_VENV=true
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -q --upgrade pip
pip3 install -r requirements.txt

# Update config with detected LaTeX engine
if [ -n "$LATEX_ENGINE" ]; then
    echo ""
    echo "Updating config.yaml with LaTeX engine: $LATEX_ENGINE"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/engine: .*/engine: \"$LATEX_ENGINE\"/" config.yaml
    else
        sed -i "s/engine: .*/engine: \"$LATEX_ENGINE\"/" config.yaml
    fi
fi

# Create output directories
echo ""
echo "Creating output directories..."
mkdir -p output/papers
mkdir -p output/latex

# Make main script executable
chmod +x main.py

# Test installation
echo ""
echo "Testing installation..."
python3 main.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Installation successful!"
else
    echo "⚠ Installation test failed"
fi

echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo ""
echo "Usage:"
if [ "$USE_VENV" = true ]; then
    echo "  1. Activate virtual environment:"
    echo "     source venv/bin/activate"
fi
echo "  2. Run the collector:"
echo "     python3 main.py --run"
echo ""
echo "  3. Edit keywords:"
echo "     python3 main.py --edit-keywords"
echo ""
echo "  4. Start scheduled daemon:"
echo "     python3 main.py --daemon"
echo ""
echo "For more information, see README.md"
