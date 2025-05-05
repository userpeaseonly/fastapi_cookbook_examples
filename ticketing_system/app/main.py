from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from typing import Annotated
from app.database import Base
from app.db_connection import (AsyncSessionLocal, get_engine, get_db_sesion)
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.operations import create_ticket

class TicketRequest(BaseModel):
    price: float | None
    show: str | None
    user: str | None = None



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    This function is called when the application starts up and shuts down.
    """
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()



app = FastAPI(lifespan=lifespan)


@app.post("/ticket", response_model=dict[str, int])
async def create_ticket_route(
    ticket: TicketRequest,
    db_session: Annotated[AsyncSession, Depends(get_db_sesion)]
):
    ticket_id = await create_ticket(
        db_session,
        ticket.show,
        ticket.user,
        ticket.price
    )
    return {"ticket_id": ticket_id}