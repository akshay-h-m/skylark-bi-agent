import requests
from .config import MONDAY_API_KEY

URL = "https://api.monday.com/v2"


def fetch_board(board_id: int):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        columns {{
          id
          title
        }}
        items_page {{
          items {{
            id
            name
            column_values {{
              id
              text
            }}
          }}
        }}
      }}
    }}
    """

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(URL, json={"query": query}, headers=headers)

    data = response.json()

    if "errors" in data:
        raise Exception(data["errors"])

    board = data["data"]["boards"][0]

    return {
        "columns": board["columns"],
        "items": board["items_page"]["items"]
    }

