"""
PDF Compiler Module
Compiles LaTeX documents to PDF using pdflatex
"""

import os
import subprocess
import tempfile
import shutil
from typing import Optional, List
import logging
from pathlib import Path


class PdfCompiler:
    """Compiles LaTeX documents to PDF"""

    def __init__(
        self,
        engine: str = "pdflatex",
        max_compile_time: int = 60,
        attempts: int = 2
    ):
        """
        Initialize the PDF compiler

        Args:
            engine: LaTeX engine to use (pdflatex, xelatex, lualatex)
            max_compile_time: Maximum compilation time in seconds
            attempts: Number of compilation attempts
        """
        self.engine = engine
        self.max_compile_time = max_compile_time
        self.attempts = attempts
        self.logger = logging.getLogger(__name__)

    def compile(
        self,
        latex_file: str,
        output_dir: Optional[str] = None,
        clean_aux: bool = True
    ) -> Optional[str]:
        """
        Compile LaTeX file to PDF

        Args:
            latex_file: Path to the LaTeX file
            output_dir: Directory for output PDF (same as latex_file if None)
            clean_aux: Whether to clean auxiliary files

        Returns:
            Path to the generated PDF, or None if compilation failed
        """
        latex_path = Path(latex_file)
        if not latex_path.exists():
            self.logger.error(f"LaTeX file not found: {latex_file}")
            return None

        if output_dir is None:
            output_dir = latex_path.parent
        else:
            os.makedirs(output_dir, exist_ok=True)

        self.logger.info(f"Compiling {latex_file} using {self.engine}")

        # Check if LaTeX engine is available
        if not self._check_engine():
            self.logger.error(f"LaTeX engine '{self.engine}' not found. Please install LaTeX (e.g., TeX Live or MiKTeX)")
            return None

        # Run LaTeX compilation (may need multiple passes for references)
        for attempt in range(self.attempts):
            success = self._run_compilation(latex_path, output_dir, attempt + 1)
            if not success:
                self.logger.error(f"Compilation failed on attempt {attempt + 1}")
                return None

        # Find the generated PDF
        pdf_path = latex_path.with_suffix('.pdf')
        if output_dir != latex_path.parent:
            target_pdf = Path(output_dir) / latex_path.with_suffix('.pdf').name
            shutil.move(str(pdf_path), str(target_pdf))
            pdf_path = target_pdf

        if pdf_path.exists():
            self.logger.info(f"PDF generated successfully: {pdf_path}")

            # Clean auxiliary files if requested
            if clean_aux:
                self._clean_aux_files(latex_path.with_suffix(''))

            return str(pdf_path)
        else:
            self.logger.error("PDF file was not generated")
            return None

    def _run_compilation(
        self,
        latex_path: Path,
        output_dir: str,
        attempt: int
    ) -> bool:
        """
        Run a single LaTeX compilation attempt

        Args:
            latex_path: Path to the LaTeX file
            output_dir: Output directory
            attempt: Attempt number

        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                self.engine,
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={output_dir}",
                str(latex_path)
            ]

            self.logger.debug(f"Running compilation attempt {attempt}: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.max_compile_time,
                cwd=latex_path.parent
            )

            # Check for errors in output
            if result.returncode != 0:
                self.logger.error(f"Compilation error (attempt {attempt}):")
                self._log_compilation_errors(result.stdout)
                return False

            # Check for fatal errors
            if "Fatal error" in result.stdout or "! Emergency stop" in result.stdout:
                self.logger.error(f"Fatal error in LaTeX compilation (attempt {attempt})")
                self._log_compilation_errors(result.stdout)
                return False

            self.logger.debug(f"Compilation attempt {attempt} completed")
            return True

        except subprocess.TimeoutExpired:
            self.logger.error(f"Compilation timed out after {self.max_compile_time} seconds")
            return False
        except Exception as e:
            self.logger.error(f"Compilation error: {e}")
            return False

    def _check_engine(self) -> bool:
        """
        Check if the LaTeX engine is available

        Returns:
            True if engine is found, False otherwise
        """
        try:
            result = subprocess.run(
                [self.engine, "--version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _log_compilation_errors(self, output: str):
        """
        Log relevant compilation errors from LaTeX output

        Args:
            output: LaTeX output text
        """
        lines = output.split('\n')
        error_lines = []

        for line in lines:
            line = line.strip()
            # Skip non-error lines
            if not line or line.startswith('Underfull') or line.startswith('Overfull'):
                continue
            if line.startswith('!') or line.startswith('l.') or 'Error' in line:
                error_lines.append(line)

        if error_lines:
            # Show last 10 error lines
            for line in error_lines[-10:]:
                self.logger.error(f"  {line}")

    def _clean_aux_files(self, base_path: Path):
        """
        Clean auxiliary LaTeX files

        Args:
            base_path: Base path of the LaTeX file (without extension)
        """
        aux_extensions = [
            '.aux', '.log', '.out', '.toc', '.lof', '.lot',
            '.fls', '.fdb_latexmk', '.synctex.gz', '.bbl', '.blg'
        ]

        for ext in aux_extensions:
            aux_file = base_path.with_suffix(ext)
            if aux_file.exists():
                try:
                    aux_file.unlink()
                    self.logger.debug(f"Cleaned auxiliary file: {aux_file}")
                except Exception as e:
                    self.logger.warning(f"Could not clean {aux_file}: {e}")

    def batch_compile(
        self,
        latex_files: List[str],
        output_dir: Optional[str] = None
    ) -> List[str]:
        """
        Compile multiple LaTeX files

        Args:
            latex_files: List of LaTeX file paths
            output_dir: Common output directory

        Returns:
            List of successfully generated PDF paths
        """
        successful = []

        for latex_file in latex_files:
            pdf_path = self.compile(latex_file, output_dir)
            if pdf_path:
                successful.append(pdf_path)

        self.logger.info(f"Batch compilation: {len(successful)}/{len(latex_files)} successful")

        return successful
