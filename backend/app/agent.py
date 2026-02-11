from datetime import datetime
import pandas as pd
import re
from .bi_engine import compute_metrics
from .llm import ask_llm


# ---------------------------------------
# Sector Filter (Deals)
# ---------------------------------------
def filter_by_sector(query, deals_df):
    q = query.lower()

    sector_col = next(
        (c for c in deals_df.columns if "sector" in c.lower()),
        None
    )

    if not sector_col:
        return deals_df, None

    unique_sectors = deals_df[sector_col].dropna().unique()

    for sector in unique_sectors:
        if str(sector).lower() in q:
            filtered = deals_df[deals_df[sector_col] == sector]
            return filtered, sector

    return deals_df, None


# ---------------------------------------
# Quarter Filter (Deals)
# ---------------------------------------
def filter_by_quarter(query, deals_df):
    q = query.lower()

    date_col = next(
        (c for c in deals_df.columns if "date" in c.lower()),
        None
    )

    if not date_col:
        return deals_df, None, None, None

    deals_df[date_col] = pd.to_datetime(
        deals_df[date_col], errors="coerce"
    )

    now = datetime.now()
    current_year = now.year
    current_quarter = (now.month - 1) // 3 + 1

    target_quarter = None
    target_year = current_year

    # -------------------------
    # Detect explicit year (e.g., 2024)
    # -------------------------
    year_match = re.search(r"(20\d{2})", q)
    if year_match:
        target_year = int(year_match.group(1))

    # -------------------------
    # Detect quarter
    # -------------------------
    if "last quarter" in q or "previous quarter" in q:
        target_quarter = current_quarter - 1
        if target_quarter == 0:
            target_quarter = 4
            target_year = current_year - 1

    elif "this quarter" in q or "current quarter" in q:
        target_quarter = current_quarter

    elif "q1" in q:
        target_quarter = 1
    elif "q2" in q:
        target_quarter = 2
    elif "q3" in q:
        target_quarter = 3
    elif "q4" in q:
        target_quarter = 4

    if not target_quarter:
        return deals_df, None, None, None

    # -------------------------
    # Build date range
    # -------------------------
    start_month = (target_quarter - 1) * 3 + 1
    start_date = datetime(target_year, start_month, 1)

    if target_quarter == 4:
        end_date = datetime(target_year + 1, 1, 1)
    else:
        end_date = datetime(target_year, start_month + 3, 1)

    filtered = deals_df[
        (deals_df[date_col] >= start_date) &
        (deals_df[date_col] < end_date)
    ]

    return filtered, f"Q{target_quarter} {target_year}", start_date, end_date


# ---------------------------------------
# MAIN QUERY HANDLER
# ---------------------------------------
def handle_query(query, deals_df, work_df):

    # -----------------------
    # Apply Sector Filter (Deals)
    # -----------------------
    deals_df, sector_used = filter_by_sector(query, deals_df)

    # Apply same sector filter to Work Orders
    if sector_used:
        wo_sector_col = next(
            (c for c in work_df.columns if "sector" in c.lower()),
            None
        )
        if wo_sector_col:
            work_df = work_df[work_df[wo_sector_col] == sector_used]

    # -----------------------
    # Apply Quarter Filter (Deals)
    # -----------------------
    deals_df, quarter_used, start_date, end_date = filter_by_quarter(query, deals_df)

    # Apply same quarter filter to Work Orders
    if quarter_used and start_date and end_date:
        wo_date_col = next(
            (c for c in work_df.columns if "date" in c.lower()),
            None
        )

        if wo_date_col:
            work_df[wo_date_col] = pd.to_datetime(
                work_df[wo_date_col], errors="coerce"
            )

            work_df = work_df[
                (work_df[wo_date_col] >= start_date) &
                (work_df[wo_date_col] < end_date)
            ]

    # -----------------------
    # Compute Metrics AFTER Filtering
    # -----------------------
    metrics = compute_metrics(deals_df, work_df)

    # -----------------------
    # Build Context Note
    # -----------------------
    context_note = ""

    if sector_used:
        context_note += f"\nFiltered by sector: {sector_used}"

    if quarter_used:
        context_note += f"\nFiltered by quarter: {quarter_used}"

    if not context_note:
        context_note = "No additional filters applied."

    # -----------------------
    # Build LLM Prompt
    # -----------------------
    prompt = f"""
The following metrics are final and authoritative.
Treat them as immutable financial statements.
You are a Founder-level Business Intelligence AI Agent.

IMPORTANT RULES:
1. You MUST use numbers exactly as provided.
2. Do NOT convert units (no millions, billions, etc.).
3. Do NOT round values unless already rounded.
4. Use numbers exactly as provided.They are already properly formatted.

5. Do NOT calculate new percentages.
6. If total_pipeline = 0, clearly state no data.

The following metrics are final and authoritative.
Treat them as immutable financial statements.

Structured Company Metrics:
{metrics}

Context:
{context_note}

Formatting Rules:
- Adapt structure based on the question.
- If question is strategic (e.g., "Is pipeline healthy?"), include Risks and Recommendations.
- If question is focused (e.g., "What are the risks?"), answer directly without repeating full metrics.
- If question is numeric (e.g., "Which stage highest?"), provide concise answer with key value.
- Avoid repeating full breakdown unless explicitly requested.
.

Instructions:
- Answer analytically.
- Highlight concentration risks if >50%.
- Be executive and concise.
- Do not invent numbers.
- If no data exists, clearly state it.

Founder Question:
{query}

Answer:
"""

    return ask_llm(prompt)
