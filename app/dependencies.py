from typing import Annotated
from fastapi import Header, HTTPException

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "supabase-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "App-Prove":
        raise HTTPException(status_code=400, detail="No App-Prove token provided")