from fastapi import HTTPException, Depends
from datetime import date
from datetime import date, timedelta
from fastapi import Query
from typing import Tuple


def check_start_end_condition(start: date, end: date):
    if end and end < start:
        raise HTTPException(
            status_code=400,
            detail="End date must be "
            "greater than or equal to start date.",
        )


def time_range(
    start: date | None = Query(
        default=date.today(),
        description="If not provided the current date is used",
        examples=date.today().isoformat(),
    ),
    end: date | None = Query(
        default=None,
        examples=date.today() + timedelta(days=7),
    )
) -> Tuple[date, date | None]:
    check_start_end_condition(start, end)
    return start, end
