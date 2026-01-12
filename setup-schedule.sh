#!/bin/bash
# ArXiv Paper Collector - Scheduler Setup Script
# Automatically configures daily scheduled execution

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================="
echo "ArXiv Paper Collector - Scheduler Setup"
echo "=================================="
echo ""

# Get current user
CURRENT_USER=$(whoami)
PYTHON_CMD=$(which python3)

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="linux"
else
    PLATFORM="unknown"
fi

echo "Detected platform: $PLATFORM"
echo "Current user: $CURRENT_USER"
echo "Python: $PYTHON_CMD"
echo ""

# Read schedule time from config
HOUR=$(grep -A1 "schedule:" config.yaml | grep "hour:" | awk '{print $2}' | tr -d '"')
MINUTE=$(grep -A2 "schedule:" config.yaml | grep "minute:" | awk '{print $2}' | tr -d '"')

echo "Scheduled time: ${HOUR}:${MINUTE} (from config.yaml)"
echo ""

# Check if running with cron
if [ "$PLATFORM" = "linux" ] || [ "$PLATFORM" = "macos" ]; then
    echo "=== Setting up cron job ==="

    # Check if cron entry already exists
    if crontab -l 2>/dev/null | grep -q "arxiv-paper-collector"; then
        echo "⚠ Found existing cron job"
        read -p "Remove old entry and reinstall? (y/N): " -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Remove old entry
            crontab -l | grep -v "arxiv-paper-collector" | crontab -
            echo "Old cron entry removed"
        else
            echo "Keeping existing cron job"
            exit 0
        fi
    fi

    # Create temporary cron file
    TEMP_CRON=$(mktemp)
    crontab -l > "$TEMP_CRON" 2>/dev/null || true

    # Add new cron entry
    echo "# ArXiv Paper Collector - Daily at ${HOUR}:${MINUTE}" >> "$TEMP_CRON"
    echo "${MINUTE} ${HOUR} * * * cd ${SCRIPT_DIR} && ${PYTHON_CMD} main.py --run >> output/cron.log 2>&1" >> "$TEMP_CRON"

    # Install new crontab
    crontab "$TEMP_CRON"
    rm "$TEMP_CRON"

    echo "✓ Cron job installed successfully!"
    echo "  Schedule: Daily at ${HOUR}:${MINUTE}"
    echo "  Log file: output/cron.log"
    echo ""
    echo "To view cron jobs: crontab -l"
    echo "To remove: crontab -e (and delete the relevant lines)"

elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "=== Setting up LaunchAgent (macOS) ==="

    PLIST_PATH="$HOME/Library/LaunchAgents/com.arxivcollector.plist"

    # Create plist file
    cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.arxivcollector</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_CMD}</string>
        <string>${SCRIPT_DIR}/main.py</string>
        <string>--run</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>${HOUR}</integer>
        <key>Minute</key>
        <integer>${MINUTE}</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>${SCRIPT_DIR}/output/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>${SCRIPT_DIR}/output/launchd.error.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

    # Load the LaunchAgent
    launchctl load "$PLIST_PATH" 2>/dev/null || echo "Note: LaunchAgent will load on next login"

    echo "✓ LaunchAgent installed: $PLIST_PATH"
    echo "  Schedule: Daily at ${HOUR}:${MINUTE}"
    echo ""
    echo "To unload: launchctl unload $PLIST_PATH"
    echo "To view logs: tail -f output/launchd.log"

fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "The collector will run automatically every day at ${HOUR}:${MINUTE}"
echo ""
echo "To test immediately:"
echo "  ${PYTHON_CMD} main.py --run"
echo ""
echo "To view logs:"
echo "  tail -f output/cron.log"
echo ""
