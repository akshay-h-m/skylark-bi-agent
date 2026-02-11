import os
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
DEALS_BOARD_ID = int(os.getenv("DEALS_BOARD_ID"))
WORK_ORDERS_BOARD_ID = int(os.getenv("WORK_ORDERS_BOARD_ID"))
HF_API_KEY = os.getenv("HF_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
