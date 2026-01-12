"""
Scheduler Module
Handles scheduling of paper collection tasks
"""

import schedule
import time
import threading
from datetime import datetime
from typing import Callable, Optional
import logging


class PaperScheduler:
    """Schedules automated paper collection tasks"""

    def __init__(self, hour: int = 10, minute: int = 0):
        """
        Initialize the scheduler

        Args:
            hour: Hour to run the task (0-23)
            minute: Minute to run the task (0-59)
        """
        self.hour = hour
        self.minute = minute
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def schedule_daily(self, task: Callable):
        """
        Schedule a task to run daily at the specified time

        Args:
            task: Callable function to execute
        """
        schedule.every().day.at(f"{self.hour:02d}:{self.minute:02d}").do(task)
        self.logger.info(f"Scheduled task to run daily at {self.hour:02d}:{self.minute:02d}")

    def schedule_interval(self, task: Callable, interval_minutes: int):
        """
        Schedule a task to run at regular intervals

        Args:
            task: Callable function to execute
            interval_minutes: Interval in minutes
        """
        schedule.every(interval_minutes).minutes.do(task)
        self.logger.info(f"Scheduled task to run every {interval_minutes} minutes")

    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            self.logger.warning("Scheduler is already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        self.logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()
        if self.thread:
            self.thread.join(timeout=5)
        self.logger.info("Scheduler stopped")

    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")

    def run_now(self, task: Callable):
        """
        Run a task immediately

        Args:
            task: Callable function to execute
        """
        self.logger.info("Running task immediately")
        try:
            task()
        except Exception as e:
            self.logger.error(f"Error running task: {e}")

    def get_next_run_time(self) -> Optional[datetime]:
        """
        Get the next scheduled run time

        Returns:
            Next run time as datetime, or None if no jobs scheduled
        """
        next_run = schedule.next_run()
        if next_run:
            return next_run
        return None

    @staticmethod
    def create_cron_entry(hour: int = 10, minute: int = 0, script_path: str = "main.py") -> str:
        """
        Generate a crontab entry for the task

        Args:
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
            script_path: Path to the Python script

        Returns:
            Crontab entry string
        """
        return f"{minute} {hour} * * * cd /path/to/arxiv-paper-collector && /usr/bin/python3 {script_path} >> output/cron.log 2>&1"

    @staticmethod
    def get_systemd_service_content(project_path: str = "/path/to/arxiv-paper-collector") -> str:
        """
        Generate a systemd service file content

        Args:
            project_path: Path to the project directory

        Returns:
            Systemd service file content
        """
        return f"""[Unit]
Description=ArXiv Paper Collector Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory={project_path}
ExecStart=/usr/bin/python3 {project_path}/main.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
