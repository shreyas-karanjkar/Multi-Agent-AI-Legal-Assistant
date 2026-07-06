"""
legal_precedent_tool.py
------------------------
Legal precedent search using DuckDuckGo.
Uses the duckduckgo-search library (pip install duckduckgo-search).
"""

import time
from typing import Type, Optional

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

try:
    from duckduckgo_search import DDGS
    DDG_AVAILABLE = True
except ImportError:
    DDG_AVAILABLE = False


# ── Pydantic Input Schema ─────────────────────────────────────────────────────

class LegalPrecedentInput(BaseModel):
    query: str = Field(
        ...,
        description=(
            "A specific legal query for finding court judgments and case precedents. "
            "Include crime type, IPC section number, and 'India' for best results. "
            "Example: 'India Supreme Court IPC Section 498A domestic violence landmark case judgment'"
        ),
    )
    max_results: Optional[int] = Field(
        default=2,
        description="Maximum number of precedent results to return (default 2).",
    )


# ── Trusted Indian legal sites to prioritise ─────────────────────────────────
LEGAL_SITES = [
    "site:indiankanoon.org",
    "site:livelaw.in",
    "site:barandbench.com",
    "site:sci.gov.in",
    "site:legalbites.in",
]


# ── CrewAI Tool ───────────────────────────────────────────────────────────────

class LegalPrecedentSearchTool(BaseTool):
    """
    Web search tool for legal precedents using DuckDuckGo.
    Searches Indian legal databases for court judgments and landmark cases.
    """

    name: str = "Legal Precedent Search Tool"
    description: str = (
        "Use this tool to search for relevant legal precedents, past court judgments, "
        "and landmark cases from Indian courts (Supreme Court, High Courts) "
        "related to a specific legal issue or IPC section. "
        "Uses DuckDuckGo for search."
    )
    args_schema: Type[BaseModel] = LegalPrecedentInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """Search DuckDuckGo for Indian legal precedents."""

        if not DDG_AVAILABLE:
            return (
                "duckduckgo-search library not installed.\n"
                "Run: pip install duckduckgo-search\n"
                "Then restart the app."
            )

        output_lines = ["=== LEGAL PRECEDENTS & JUDGMENTS (via DuckDuckGo) ===\n"]

        # Strategy: search multiple targeted queries across trusted legal sites
        search_attempts = [
            f"India court judgment {query} IPC section verdict",
            f"Supreme Court India {query} landmark case",
            f"High Court India {query} judgment precedent",
        ]

        seen_urls = set()
        all_results = []

        try:
            with DDGS() as ddgs:
                for attempt_query in search_attempts:
                    if len(all_results) >= max_results:
                        break
                    try:
                        results = ddgs.text(
                            keywords=attempt_query,
                            region="in-en",         # India region
                            safesearch="moderate",
                            max_results=max_results,
                        )
                        for r in results:
                            url = r.get("href", "")
                            if url not in seen_urls:
                                seen_urls.add(url)
                                all_results.append(r)
                        # Brief pause to avoid rate limiting
                        time.sleep(0.5)
                    except Exception:
                        continue

        except Exception as exc:
            # DuckDuckGo occasionally blocks automated requests temporarily
            return (
                f"DuckDuckGo search temporarily unavailable: {exc}\n\n"
                "FALLBACK — Notable Indian Legal Precedents:\n"
                + _get_fallback_precedents(query)
            )

        if not all_results:
            return (
                "No live results found — DuckDuckGo may be rate-limiting temporarily.\n\n"
                "FALLBACK — Notable Indian Legal Precedents:\n"
                + _get_fallback_precedents(query)
            )

        for i, result in enumerate(all_results[:max_results], start=1):
            title   = result.get("title", "Untitled")
            url     = result.get("href", "N/A")
            snippet = result.get("body", "No summary available.")[:400]
            output_lines.append(
                f"[{i}] {title}\n"
                f"    Source : {url}\n"
                f"    Summary: {snippet}...\n"
            )

        return "\n".join(output_lines)


def _get_fallback_precedents(query: str) -> str:
    """
    Static fallback precedents when DuckDuckGo is unavailable.
    Covers the most common IPC scenarios.
    """
    query_lower = query.lower()

    if any(w in query_lower for w in ["murder", "302", "homicide", "death"]):
        return (
            "• K.M. Nanavati v. State of Maharashtra (1962) AIR SC 605\n"
            "  Distinguished murder from culpable homicide; established jury trial precedent.\n\n"
            "• Bachan Singh v. State of Punjab (1980) AIR SC 898\n"
            "  Laid down 'rarest of rare' doctrine for death penalty under Section 302 IPC.\n\n"
            "• Machhi Singh v. State of Punjab (1983) AIR SC 957\n"
            "  Further refined the rarest of rare doctrine; five categories of murder cases.\n"
        )
    elif any(w in query_lower for w in ["rape", "375", "sexual", "assault"]):
        return (
            "• Tukaram v. State of Maharashtra (1979) AIR SC 185 (Mathura Case)\n"
            "  Led to the Criminal Law Amendment Act 1983 strengthening rape laws.\n\n"
            "• State of Punjab v. Gurmit Singh (1996) 2 SCC 384\n"
            "  SC held that rape victim's testimony can be basis for conviction.\n\n"
            "• Mukesh & Anr v. State for NCT of Delhi (2017) 6 SCC 1 (Nirbhaya)\n"
            "  Confirmed death penalty; extensively discussed aggravated rape provisions.\n"
        )
    elif any(w in query_lower for w in ["dowry", "498", "cruelty", "domestic", "wife"]):
        return (
            "• Arnesh Kumar v. State of Bihar (2014) 8 SCC 273\n"
            "  SC issued guidelines preventing automatic arrest under Section 498A IPC.\n\n"
            "• Rajesh Sharma v. State of UP (2017) 11 SCC 444\n"
            "  Welfare committee mechanism for 498A cases; later modified by SC.\n\n"
            "• Sushil Kumar Sharma v. Union of India (2005) 6 SCC 281\n"
            "  Discussed misuse of Section 498A; SC called for balanced application.\n"
        )
    elif any(w in query_lower for w in ["fraud", "420", "cheating", "scam"]):
        return (
            "• R.K. Dalmia v. Delhi Administration (1962) AIR SC 1821\n"
            "  Landmark on criminal breach of trust and cheating under IPC.\n\n"
            "• Hridaya Ranjan Prasad Verma v. State of Bihar (2000) 4 SCC 168\n"
            "  Defined distinction between Section 415 and 420 IPC; intent is key.\n\n"
            "• Vesa Holdings v. State of Kerala (2015) 8 SCC 293\n"
            "  SC held that mere failure to repay does not constitute cheating.\n"
        )
    else:
        return (
            "• Vishaka v. State of Rajasthan (1997) 6 SCC 241\n"
            "  Established Vishaka Guidelines for workplace sexual harassment.\n\n"
            "• D.K. Basu v. State of West Bengal (1997) 1 SCC 416\n"
            "  Landmark on custodial rights; guidelines for arrest and detention.\n\n"
            "• Lalita Kumari v. Govt of UP (2014) 2 SCC 1\n"
            "  SC mandated mandatory FIR registration for cognizable offences.\n\n"
            "• State of Haryana v. Bhajan Lal (1992) Supp (1) SCC 335\n"
            "  Guidelines for quashing of FIRs; fundamental precedent in criminal law.\n"
        )
