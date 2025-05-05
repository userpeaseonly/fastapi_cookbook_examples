from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import Ticket, TicketDetails

async def create_ticket(db_session: AsyncSession, show_name: str, user: str = None, price: float = None) -> int:
    """
    Create a new ticket in the database.

    Args:
        db_session (AsyncSession): The database session to use.
        show_name (str): The name of the show.
        user (str, optional): The user associated with the ticket. Defaults to None.
        price (float, optional): The price of the ticket. Defaults to None.

    Returns:
        int: The ID of the created ticket.
    """
    ticket = Ticket(
        show=show_name,
        user=user,
        price=price,
        details=TicketDetails(),
    )
    async with db_session.begin():
        db_session.add(ticket)
        await db_session.flush()
        ticket_id = ticket.id
        await db_session.commit()
    return ticket_id



async def get_ticket(
    db_session: AsyncSession,
    ticket_id: int,
) -> Ticket | None:
    query = (
        select(Ticket).where(Ticket.id == ticket_id)
    )
    async with db_session as session:
        tickets = await session.execute(query)
        return tickets.scalars().first()


async def update_ticket_price(
    db_session: AsyncSession,
    ticket_id: int,
    new_price: float,
) -> bool:
    """
    Update the price of a ticket in the database.

    Args:
        db_session (AsyncSession): The database session to use.
        ticket_id (int): The ID of the ticket to update.
        new_price (float): The new price for the ticket.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = (
        update(Ticket).where(Ticket.id == ticket_id).values(price=new_price)
    )
    async with db_session as session:
        ticket_updated = await session.execute(query)
        await session.commit()
        return ticket_updated.rowcount != 0


async def delete_ticket(db_session: AsyncSession, ticket_id: int) -> bool:
    async with db_session as session:
        tickets_removed = await session.execute(
            delete(
                Ticket
            ).where(Ticket.id == ticket_id)
        )
        await session.commit()
        return tickets_removed.rowcount != 0


async def update_ticket_details(db_session: AsyncSession, ticket_id: int, updating_ticket_details: dict) -> bool:
    ticket_query = update(TicketDetails).where(TicketDetails.ticket.id == ticket_id)
    if updating_ticket_details != {}:
        ticket_query = ticket_query.values(
            *updating_ticket_details
        )
        result = await db_session.execute(
            ticket_query
        )
        await db_session.commit()
        if result.rowcount == 0:
            return False
    return True


async def sell_ticket_to_user(
    db_session: AsyncSession, ticket_id: int, user: str
) -> bool:
    ticket_query = (
        update(Ticket)
        .where(
            and_(
                Ticket.id == ticket_id,
                Ticket.sold == False,
            )
        )
        .values(user=user, sold=True)
    )
    async with db_session as session:
        result = (
            await db_session.execute(ticket_query)
        )
        await db_session.commit()
        if result.rowcount == 0:
            return False
    return True