"""
company_data.py - the workshop's private business data (provided - nothing to merge)

Three fictional companies, their recent news, and a house style guide. A
language model can't know any of this on its own, so agents have to use
tools to get it. Each lab wraps these plain functions as tools for its
framework (LangGraph, CrewAI, ...).
"""

PROFILES = {
    "acme corp": ("Acme Corp is headquartered in Portland, Oregon and makes outdoor "
                  "camping gear. It has 1200 employees. Revenue: $120 million in 2022, "
                  "$180 million in 2025."),
    "globex": ("Globex is headquartered in Berlin, Germany and makes industrial "
               "robots. It has 5400 employees. Revenue: $820 million in 2022, "
               "$950 million in 2025."),
    "initech": ("Initech is headquartered in Austin, Texas and makes payroll "
                "software. It has 350 employees. Revenue: $40 million in 2022, "
                "$95 million in 2025."),
}

NEWS = {
    "acme corp": [
        "Aug 2026: Acme Corp opens a second factory in Columbus, Ohio, doubling its production capacity.",
        "Mar 2026: Acme Corp recalls 2,000 camping stoves over a faulty gas valve; no injuries were reported.",
    ],
    "globex": [
        "Sep 2026: Globex wins a $200 million contract to supply welding robots to a European carmaker.",
        "Jun 2026: Globex's CEO steps down; the CFO is acting CEO while the board searches for a replacement.",
    ],
    "initech": [
        "Oct 2026: Initech signs 40 new enterprise customers in one quarter, a company record.",
        "Jul 2026: A 6-hour Initech outage delays payroll for about 300 client companies.",
    ],
}

STYLE_GUIDES = {
    "board": ("Board/executive style: open with a one-sentence recommendation. Then at "
              "most 3 bullet points, each containing a number. No jargon. Under 100 words."),
    "investor": ("Investor style: open with revenue and growth figures, then the main "
                 "risks. Neutral tone - never tell the reader to buy or sell. Under 120 words."),
    "engineering": ("Engineering style: focus on products, capacity, and reliability "
                    "incidents. Plain sentences with specific numbers. Under 120 words."),
}
_AUDIENCE_WORDS = {
    "board": "board", "executive": "board", "leadership": "board", "ceo": "board",
    "investor": "investor", "investors": "investor", "finance": "investor",
    "engineering": "engineering", "engineers": "engineering", "technical": "engineering",
}


def _key(name):
    return name.strip().lower().rstrip(".")


def lookup_company(name: str) -> str:
    """Profile and financials for one company (Acme Corp, Globex, or Initech)."""
    return PROFILES.get(_key(name), f"No profile found for {name}. "
                        f"Known companies: Acme Corp, Globex, Initech.")


def get_news(company: str) -> str:
    """Recent news headlines for one company (Acme Corp, Globex, or Initech)."""
    items = NEWS.get(_key(company))
    if not items:
        return f"No news found for {company}. Known companies: Acme Corp, Globex, Initech."
    return "\n".join(items)


def get_style_guide(audience: str) -> str:
    """House writing rules for an audience: board, investor, or engineering."""
    for word in _key(audience).replace("/", " ").replace("-", " ").split():
        if word in _AUDIENCE_WORDS:
            return STYLE_GUIDES[_AUDIENCE_WORDS[word]]
    return ("No style guide for that audience. Available: board (executives), "
            "investor, engineering.")


def calculate(expression: str) -> str:
    """Evaluate an arithmetic expression exactly, e.g. '950000000 / 5400' or a
    yearly growth rate like '(95 / 40) ** (1 / 3) - 1'."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Only basic arithmetic is supported."
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Could not evaluate: {e}"
