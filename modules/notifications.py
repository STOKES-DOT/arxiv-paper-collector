"""
Notification Module
Supports email and system notifications for completed collections
"""

import os
import smtplib
import subprocess
import platform
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging


class NotificationManager:
    """Manages notifications for paper collection completion"""

    def __init__(self, config: dict = None):
        """
        Initialize notification manager

        Args:
            config: Configuration dictionary with notification settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

    def send_notification(
        self,
        num_papers: int,
        pdf_path: str,
        error: Optional[str] = None
    ) -> bool:
        """
        Send notification based on configured methods

        Args:
            num_papers: Number of papers collected
            pdf_path: Path to generated PDF
            error: Error message if collection failed

        Returns:
            True if notification was sent successfully
        """
        success = False

        # Determine message content
        if error:
            title = "ArXiv Paper Collection - Failed"
            message = f"Paper collection failed with error:\n\n{error}"
        else:
            title = "ArXiv Paper Collection - Completed"
            message = f"Successfully collected {num_papers} papers\n\nPDF: {pdf_path}"

        # Send system notification
        if self.config.get("system_notification", True):
            success |= self._send_system_notification(title, message)

        # Send email notification
        if self.config.get("email_enabled", False):
            success |= self._send_email(title, message)

        return success

    def _send_system_notification(self, title: str, message: str) -> bool:
        """
        Send desktop system notification

        Args:
            title: Notification title
            message: Notification message

        Returns:
            True if successful
        """
        try:
            system = platform.system()

            if system == "Darwin":  # macOS
                # Use osascript for macOS notifications
                cmd = [
                    "osascript", "-e",
                    f'display notification "{message}" with title "{title}" sound name "default"'
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                return True

            elif system == "Linux":
                # Check for notify-send
                if self._command_exists("notify-send"):
                    cmd = [
                        "notify-send",
                        title,
                        message,
                        "-i", "dialog-information"
                    ]
                    subprocess.run(cmd, check=True, capture_output=True)
                    return True
                else:
                    self.logger.warning("notify-send not found. Install: sudo apt-get install libnotify-bin")
                    return False

            elif system == "Windows":
                # Use Windows toast notification
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        title,
                        message,
                        duration=10,
                        threaded=True
                    )
                    return True
                except ImportError:
                    self.logger.warning("win10toast not installed. Install: pip install win10toast")
                    return False

        except Exception as e:
            self.logger.error(f"System notification failed: {e}")

        return False

    def _send_email(self, subject: str, body: str) -> bool:
        """
        Send email notification

        Args:
            subject: Email subject
            body: Email body

        Returns:
            True if successful
        """
        try:
            # Get email settings from config
            smtp_server = self.config.get("smtp_server", "smtp.gmail.com")
            smtp_port = self.config.get("smtp_port", 587)
            email_from = self.config.get("email_from")
            email_to = self.config.get("email_to")
            email_password = self.config.get("email_password")

            if not all([email_from, email_to, email_password]):
                self.logger.warning("Email configuration incomplete. Skipping email notification.")
                return False

            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = email_to
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(email_from, email_password)
                server.send_message(msg)

            self.logger.info(f"Email notification sent to {email_to}")
            return True

        except Exception as e:
            self.logger.error(f"Email notification failed: {e}")
            return False

    @staticmethod
    def _command_exists(command: str) -> bool:
        """Check if a command exists on the system"""
        try:
            subprocess.run(
                ["which", command],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def get_email_config_template() -> dict:
        """Get template for email configuration"""
        return {
            "notifications": {
                "system_notification": True,
                "email_enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "email_from": "your-email@gmail.com",
                "email_to": "your-email@gmail.com",
                "email_password": "your-app-password"  # Use app-specific password
            }
        }


def send_test_notification(config: dict = None) -> bool:
    """
    Send a test notification to verify setup

    Args:
        config: Notification configuration

    Returns:
        True if test notification was sent
    """
    manager = NotificationManager(config)
    return manager.send_notification(
        num_papers=0,
        pdf_path="test.pdf",
        error=None
    )
