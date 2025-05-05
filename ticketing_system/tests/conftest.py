import pytest
from app.database import Ticket, TicketDetails


@pytest.fixture
async def add_special_ticket(db_session_test):
    ticket = Ticket(
        id=1234,
        show="Special Show",
        details=TicketDetails(),
    )
    async with db_session_test.begin():
        db_session_test.add(ticket)
        await db_session_test.commit()