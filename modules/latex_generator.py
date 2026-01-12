"""
LaTeX Generator Module
Generates LaTeX document from paper data
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
from jinja2 import Environment, FileSystemLoader, Template
import logging


class LatexGenerator:
    """Generates LaTeX document from paper data"""

    def __init__(self, template_dir: str = "templates", template_name: str = "paper_report.tex"):
        """
        Initialize the LaTeX generator

        Args:
            template_dir: Directory containing LaTeX templates
            template_name: Name of the template file
        """
        self.template_dir = template_dir
        self.template_name = template_name
        self.logger = logging.getLogger(__name__)

        # Setup Jinja2 environment with LaTeX-friendly settings
        self.env = None
        self._setup_environment()

    def _setup_environment(self):
        """Setup Jinja2 environment with LaTeX-specific settings"""
        try:
            template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.template_dir)
            self.env = Environment(
                loader=FileSystemLoader(template_path),
                autoescape=False,
                trim_blocks=True,
                lstrip_blocks=True
            )

            # Add custom filters for LaTeX
            self.env.filters['latex_escape'] = self._latex_escape
            self.env.filters['truncate_latex'] = self._truncate_latex
            self.env.filters['format_date'] = self._format_date

            self.logger.info(f"Jinja2 environment initialized with template path: {template_path}")

        except Exception as e:
            self.logger.error(f"Error setting up Jinja2 environment: {e}")
            # Create a basic environment with default template
            self.env = Environment()
            self.env.filters['latex_escape'] = self._latex_escape
            self.env.filters['truncate_latex'] = self._truncate_latex
            self.env.filters['format_date'] = self._format_date

    @staticmethod
    def _latex_escape(text: str) -> str:
        """
        Escape special LaTeX characters

        Args:
            text: Text to escape

        Returns:
            Escaped text safe for LaTeX
        """
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\^{}',
            '\\': r'\textbackslash{}',
        }

        for char, escaped in replacements.items():
            text = text.replace(char, escaped)

        return text

    @staticmethod
    def _truncate_latex(text: str, max_length: int = 500, suffix: str = "...") -> str:
        """
        Truncate text for LaTeX display

        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def _format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
        """
        Format date for LaTeX display

        Args:
            date: Datetime object
            format_str: Format string

        Returns:
            Formatted date string
        """
        return date.strftime(format_str)

    def generate_latex(
        self,
        papers: Dict[str, List[Dict]],
        output_path: str,
        title: Optional[str] = None,
        max_papers: int = 50,
        abstract_max_length: int = 1000
    ) -> str:
        """
        Generate LaTeX document from paper data

        Args:
            papers: Dictionary of grouped papers
            output_path: Path to save the LaTeX file
            title: Optional custom title
            max_papers: Maximum number of papers per group
            abstract_max_length: Maximum abstract length

        Returns:
            Path to the generated LaTeX file
        """
        self.logger.info(f"Generating LaTeX document with {len(papers)} groups")

        # Prepare data for template
        total_papers = sum(len(paper_list) for paper_list in papers.values())

        # Sort groups and apply max papers limit
        sorted_groups = {}
        for group_name, paper_list in papers.items():
            sorted_groups[group_name] = paper_list[:max_papers]

        # Template context
        context = {
            "title": title or f"ArXiv Papers Report - {datetime.now().strftime('%Y-%m-%d')}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "groups": sorted_groups,
            "total_papers": total_papers,
            "total_groups": len(papers),
            "abstract_max_length": abstract_max_length
        }

        # Load template
        try:
            template = self.env.get_template(self.template_name)
        except Exception as e:
            self.logger.warning(f"Could not load template: {e}. Using built-in template.")
            template = self._get_builtin_template()

        # Render LaTeX
        latex_content = template.render(**context)

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        self.logger.info(f"LaTeX document generated: {output_path}")

        return output_path

    def _get_builtin_template(self) -> Template:
        """
        Get built-in LaTeX template

        Returns:
            Jinja2 Template object
        """
        latex_template = r"""
\documentclass[10pt,a4paper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{hyperref}
\usepackage{url}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{longtable}

% Page setup
\geometry{margin=1in}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={{{ title }}},
    pdfauthor={ArXiv Paper Collector}
}

% Custom section formatting
\titleformat{\section}
  {\normalfont\Large\bfseries\color{blue}}{\thesection}{1em}{}
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{darkgray}}{\thesubsection}{1em}{}

% Title info
\title{ {{ title }} }
\author{ {{ date }} }
\date{}

\begin{document}

\maketitle

\section*{Summary}
\begin{itemize}
    \item Total Papers: {{ total_papers }}
    \item Groups: {{ total_groups }}
    \item Generated: {{ date }}
\end{itemize}

\hrule
\vspace{1em}

{% for group_name, papers in groups.items() -%}
{% if papers -%}
\section{{{ group_name|latex_escape|replace('_', ' ')|title }}}

{% for paper in papers -%}
\subsection*{{{ paper.title|latex_escape }}}

\textbf{Authors:} {{ paper.authors|join(', ')|latex_escape }} \\[0.5em]

\textbf{arXiv ID:} \href{{{ paper.url }}}{{{ paper.arxiv_id }}} \\[0.5em]

\textbf{Published:} {{ paper.published|format_date }} \\[0.5em]

\textbf{Categories:} {{ paper.categories|join(', ') }} \\[1em]

\textbf{Abstract:}

{{ paper.summary|latex_escape|truncate_latex(abstract_max_length) }}

\vspace{1em}
\hrule
\vspace{1em}

{% endfor -%}
{% endif -%}
{% endfor -%}

\end{document}
"""
        return Template(latex_template, autoescape=False)

    def generate_simple_report(
        self,
        papers: List[Dict],
        output_path: str,
        title: Optional[str] = None
    ) -> str:
        """
        Generate a simple single-section LaTeX report

        Args:
            papers: List of papers
            output_path: Path to save the LaTeX file
            title: Optional custom title

        Returns:
            Path to the generated LaTeX file
        """
        grouped_papers = {"All Papers": papers}
        return self.generate_latex(grouped_papers, output_path, title)
