from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .monday_client import fetch_board
from .data_processor import normalize
from .agent import handle_query
from .config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(q: Query):

    deals_board = fetch_board(DEALS_BOARD_ID)
    work_board = fetch_board(WORK_ORDERS_BOARD_ID)

    deals_df = normalize(deals_board)
    work_df = normalize(work_board)

    response = handle_query(q.message, deals_df, work_df)

    return {"response": response}

