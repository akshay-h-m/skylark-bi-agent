def build_leadership_update(deals_data, work_data):

    return f"""
Leadership Update

Total Pipeline: ₹{deals_data.get('total_pipeline', 0):,.2f}

Deal Status Breakdown:
{deals_data.get('status_breakdown', {})}

Sector Contribution:
{deals_data.get('sector_breakdown', {})}

Total Work Orders: {work_data.get('total_work_orders', 0)}

Execution Status:
{work_data.get('status_breakdown', {})}
"""

