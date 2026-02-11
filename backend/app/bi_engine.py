import pandas as pd


def format_number(value):
    if isinstance(value, (int, float)):
        return f"{value:,.0f}"
    return value


def compute_metrics(deals_df, work_df):

    metrics = {}

    # -----------------------
    # Identify Important Columns
    # -----------------------

    revenue_col = next((c for c in deals_df.columns if "value" in c.lower()), None)
    sector_col = next((c for c in deals_df.columns if "sector" in c.lower()), None)
    stage_col = next((c for c in deals_df.columns if "stage" in c.lower()), None)
    status_col = next((c for c in deals_df.columns if "status" in c.lower()), None)

    # -----------------------
    # Clean Revenue
    # -----------------------

    if revenue_col:
        deals_df[revenue_col] = pd.to_numeric(
            deals_df[revenue_col], errors="coerce"
        ).fillna(0)
    else:
        deals_df["__dummy_value__"] = 0
        revenue_col = "__dummy_value__"

    total_pipeline_raw = float(deals_df[revenue_col].sum())
    metrics["total_pipeline"] = format_number(total_pipeline_raw)

    # -----------------------
    # Sector Breakdown
    # -----------------------

    if sector_col:
        sector_breakdown_raw = (
            deals_df.groupby(sector_col)[revenue_col]
            .sum()
            .to_dict()
        )
    else:
        sector_breakdown_raw = {}

    sector_breakdown = {
        k: format_number(v)
        for k, v in sector_breakdown_raw.items()
    }

    metrics["sector_breakdown"] = sector_breakdown

    # Sector Percentages
    if total_pipeline_raw > 0:
        sector_percentages = {
            k: round((v / total_pipeline_raw) * 100, 2)
            for k, v in sector_breakdown_raw.items()
        }
    else:
        sector_percentages = {}

    metrics["sector_percentages"] = sector_percentages

    if sector_breakdown_raw:
        highest_sector = max(sector_breakdown_raw, key=sector_breakdown_raw.get)
        metrics["highest_sector"] = highest_sector
        metrics["highest_sector_value"] = format_number(sector_breakdown_raw[highest_sector])
        metrics["highest_sector_percentage"] = sector_percentages.get(highest_sector, 0)
    else:
        metrics["highest_sector"] = None

    # -----------------------
    # Stage Breakdown
    # -----------------------

    if stage_col:
        stage_breakdown_raw = (
            deals_df.groupby(stage_col)[revenue_col]
            .sum()
            .to_dict()
        )
    else:
        stage_breakdown_raw = {}

    stage_breakdown = {
        k: format_number(v)
        for k, v in stage_breakdown_raw.items()
    }

    metrics["stage_breakdown"] = stage_breakdown

    if stage_breakdown_raw:
        highest_stage = max(stage_breakdown_raw, key=stage_breakdown_raw.get)
        metrics["highest_stage"] = highest_stage
        metrics["highest_stage_value"] = format_number(stage_breakdown_raw[highest_stage])
    else:
        metrics["highest_stage"] = None

    # -----------------------
    # Deal Status
    # -----------------------

    if status_col:
        metrics["deal_status_breakdown"] = (
            deals_df[status_col].value_counts().to_dict()
        )
    else:
        metrics["deal_status_breakdown"] = {}

    # -----------------------
    # Work Orders
    # -----------------------

    metrics["total_work_orders"] = len(work_df)

    wo_status_col = next(
        (c for c in work_df.columns if "status" in c.lower()),
        None
    )

    if wo_status_col:
        metrics["work_status_breakdown"] = (
            work_df[wo_status_col].value_counts().to_dict()
        )
    else:
        metrics["work_status_breakdown"] = {}

    return metrics
