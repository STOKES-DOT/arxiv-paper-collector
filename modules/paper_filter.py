"""
Paper Filter Module
Filters papers based on keywords and categories
"""

import re
from typing import List, Dict, Set
import logging


class PaperFilter:
    """Filters papers based on keywords and categories"""

    def __init__(self, keywords: Dict[str, List[str]]):
        """
        Initialize the paper filter

        Args:
            keywords: Dictionary of keyword groups, e.g., {
                "electronic_structure": ["DFT", "quantum chemistry"],
                "artificial_intelligence": ["machine learning", "neural network"]
            }
        """
        self.keywords = keywords
        self.logger = logging.getLogger(__name__)

    def filter_papers(self, papers: List[Dict], match_any: bool = False) -> Dict[str, List[Dict]]:
        """
        Filter papers into groups based on keyword matching

        Args:
            papers: List of paper dictionaries
            match_any: If True, paper matches if any keyword matches.
                      If False, paper must match at least one keyword from each group.

        Returns:
            Dictionary mapping group names to lists of matching papers
        """
        self.logger.info(f"Filtering {len(papers)} papers")

        grouped_papers = {}
        all_matched_papers = set()

        for group_name, group_keywords in self.keywords.items():
            matched_papers = []
            for paper in papers:
                if self._matches_keywords(paper, group_keywords):
                    matched_papers.append(paper)
                    all_matched_papers.add(id(paper))

            grouped_papers[group_name] = matched_papers
            self.logger.info(f"Group '{group_name}': {len(matched_papers)} papers matched")

        # Get papers that didn't match any group
        unmatched_papers = [
            paper for paper in papers
            if id(paper) not in all_matched_papers
        ]

        if unmatched_papers:
            grouped_papers["uncategorized"] = unmatched_papers
            self.logger.info(f"Uncategorized: {len(unmatched_papers)} papers")

        return grouped_papers

    def _matches_keywords(self, paper: Dict, keywords: List[str]) -> bool:
        """
        Check if a paper matches any of the given keywords

        Args:
            paper: Paper dictionary
            keywords: List of keywords to check

        Returns:
            True if paper matches any keyword
        """
        # Combine title and summary for searching
        text_to_search = (
            paper.get("title", "").lower() + " " +
            paper.get("summary", "").lower()
        )

        for keyword in keywords:
            if self._keyword_matches(keyword, text_to_search):
                return True

        return False

    def _keyword_matches(self, keyword: str, text: str) -> bool:
        """
        Check if a keyword matches in the text

        Args:
            keyword: Keyword to search for
            text: Text to search in

        Returns:
            True if keyword is found in text
        """
        # Exact phrase match
        if keyword.lower() in text:
            return True

        # Word boundary match
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text):
            return True

        return False

    def filter_by_relevance(self, papers: List[Dict], min_relevance: float = 0.3) -> List[Dict]:
        """
        Filter papers by relevance score based on keyword frequency

        Args:
            papers: List of paper dictionaries
            min_relevance: Minimum relevance score (0-1)

        Returns:
            List of papers with relevance >= min_relevance
        """
        scored_papers = []

        for paper in papers:
            score = self._calculate_relevance(paper)
            if score >= min_relevance:
                paper["relevance_score"] = score
                scored_papers.append(paper)

        # Sort by relevance score
        scored_papers.sort(key=lambda p: p["relevance_score"], reverse=True)

        self.logger.info(f"Filtered to {len(scored_papers)} papers with relevance >= {min_relevance}")

        return scored_papers

    def _calculate_relevance(self, paper: Dict) -> float:
        """
        Calculate relevance score for a paper based on keyword matches

        Args:
            paper: Paper dictionary

        Returns:
            Relevance score between 0 and 1
        """
        all_keywords = []
        for keyword_list in self.keywords.values():
            all_keywords.extend(keyword_list)

        # Count keyword matches
        text = (paper.get("title", "") + " " + paper.get("summary", "")).lower()
        matches = 0

        for keyword in all_keywords:
            if keyword.lower() in text:
                matches += 1

        # Calculate relevance as ratio of matched keywords to total unique keywords
        unique_keywords = len(set(all_keywords))
        if unique_keywords == 0:
            return 0.0

        return min(matches / unique_keywords, 1.0)

    def get_paper_summary(self, papers: List[Dict]) -> Dict:
        """
        Get a summary of the filtered papers

        Args:
            papers: List of paper dictionaries

        Returns:
            Summary dictionary with statistics
        """
        if not papers:
            return {
                "total": 0,
                "categories": {},
                "date_range": None
            }

        # Count by category
        category_counts = {}
        for paper in papers:
            for category in paper.get("categories", []):
                category_counts[category] = category_counts.get(category, 0) + 1

        # Get date range
        dates = [paper["published"] for paper in papers]
        date_range = {
            "earliest": min(dates),
            "latest": max(dates)
        }

        return {
            "total": len(papers),
            "categories": category_counts,
            "date_range": date_range
        }
