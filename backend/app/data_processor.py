import pandas as pd


def normalize(board_data):

    columns_meta = board_data["columns"]
    items = board_data["items"]

    # Create mapping: column_id → column_title
    id_to_title = {}
    for col in columns_meta:
        id_to_title[col["id"]] = col["title"]

    rows = []

    for item in items:
        row = {"Deal Name": item["name"]}

        for col in item["column_values"]:
            column_title = id_to_title.get(col["id"], col["id"])
            row[column_title] = col["text"]

        rows.append(row)

    df = pd.DataFrame(rows)

    # Clean whitespace
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    return df

