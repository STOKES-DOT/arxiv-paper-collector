"""
Arxiv Paper Fetcher Module
Fetches papers from arXiv API based on categories and date range
"""

import arxiv
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging


class ArxivFetcher:
    """Fetches papers from arXiv API"""

    def __init__(self, categories: List[str], days_back: int = 1, max_results: int = 100):
        """
        Initialize the arXiv fetcher

        Args:
            categories: List of arXiv categories (e.g., ["cs.AI", "physics.chem-ph"])
            days_back: Number of days back from today to search
            max_results: Maximum number of results to fetch
        """
        self.categories = categories
        self.days_back = days_back
        self.max_results = max_results
        self.logger = logging.getLogger(__name__)

    def fetch_papers(self) -> List[Dict]:
        """
        Fetch papers from arXiv published within the specified date range

        Returns:
            List of paper dictionaries containing title, authors, abstract, etc.
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.days_back)

        self.logger.info(f"Fetching papers from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

        papers = []

        # Build query string for each category
        for category in self.categories:
            query = f"cat:{category}"
            self.logger.info(f"Searching category: {category}")

            try:
                # Create search object
                search = arxiv.Search(
                    query=query,
                    max_results=self.max_results,
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )

                # Fetch results
                for result in search.results():
                    # Check if paper is within date range
                    if result.published >= start_date and result.published <= end_date:
                        paper = self._parse_paper(result)
                        papers.append(paper)

            except Exception as e:
                self.logger.error(f"Error fetching from category {category}: {e}")
                continue

        # Remove duplicates based on arXiv ID
        unique_papers = self._remove_duplicates(papers)
        self.logger.info(f"Found {len(unique_papers)} unique papers")

        return unique_papers

    def _parse_paper(self, result: arxiv.Result) -> Dict:
        """
        Parse arXiv result into a dictionary

        Args:
            result: arXiv Result object

        Returns:
            Dictionary containing paper information
        """
        return {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary.replace("\n", " "),
            "published": result.published,
            "arxiv_id": result.entry_id.split("/")[-1],
            "url": result.entry_id,
            "pdf_url": result.pdf_url,
            "categories": result.categories,
            "primary_category": result.primary_category
        }

    def _remove_duplicates(self, papers: List[Dict]) -> List[Dict]:
        """
        Remove duplicate papers based on arXiv ID

        Args:
            papers: List of paper dictionaries

        Returns:
            List of unique papers
        """
        seen_ids = set()
        unique_papers = []

        for paper in papers:
            arxiv_id = paper["arxiv_id"]
            if arxiv_id not in seen_ids:
                seen_ids.add(arxiv_id)
                unique_papers.append(paper)

        return unique_papers

    def fetch_by_keywords(self, keywords: List[str], categories: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch papers matching specific keywords

        Args:
            keywords: List of keywords to search for
            categories: Optional list of categories (uses default if not specified)

        Returns:
            List of matching papers
        """
        if categories is None:
            categories = self.categories

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.days_back)

        self.logger.info(f"Searching for keywords: {keywords}")

        papers = []

        # Build query with keywords
        query_parts = []
        for keyword in keywords:
            query_parts.append(f'all:"{keyword}"')
        query = " OR ".join(query_parts)

        # Add category filter
        cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
        full_query = f"({query}) AND ({cat_query})"

        try:
            search = arxiv.Search(
                query=full_query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )

            for result in search.results():
                if result.published >= start_date and result.published <= end_date:
                    paper = self._parse_paper(result)
                    papers.append(paper)

        except Exception as e:
            self.logger.error(f"Error fetching by keywords: {e}")

        # Remove duplicates
        unique_papers = self._remove_duplicates(papers)
        self.logger.info(f"Found {len(unique_papers)} papers matching keywords")

        return unique_papers
