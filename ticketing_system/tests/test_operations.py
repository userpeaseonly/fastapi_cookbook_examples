import asyncio
from app.operations import (
    get_ticket,
    sell_ticket_to_user,
)


async def test_concurrent_ticket_sales(
    add_special_ticket,
    db_session_test,
    second_session_test,
):
    result = await asyncio.gather(
        sell_ticket_to_user(
            db_session_test, 1234, "Jake Fake"
        ),
        sell_ticket_to_user(
            second_session_test, 1234, "John Doe"
        ),
    )
    assert result in (
        [True, False],
        [False, True],
    )  # only one of the sales should be successful
    ticket = await get_ticket(db_session_test, 1234)
    # assert that the user who bought the ticket
    # correspond to the successful sale
    if result[0]:
        assert ticket.user == "Jake Fake"
    else:
        assert ticket.user == "John Doe"