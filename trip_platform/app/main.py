from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from typing import Annotated
from app.middleware import ClientInfoMiddleware
from app.profiler import ProfileEndpontsMiddleWare
from app import internationalization
from .dependencies import time_range
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.rate_limiter import limiter
from app.background_tasks import store_query_to_external_db

import logging
logger = logging.getLogger("uvicorn.error")

app = FastAPI()
app.add_middleware(ClientInfoMiddleware)
app.add_middleware(ProfileEndpontsMiddleWare)
app.include_router(internationalization.router, prefix="/i18n", tags=["i18n"])


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/v1/trips")
def get_tours(
    time_range = Depends(time_range),
    background_tasks: BackgroundTasks = Depends,
):
    start, end = time_range
    message = f"Request trips from {start}"
    
    background_tasks.add_task(
        store_query_to_external_db, message
    )
    logger.info(f"Background task started: {message}")
    
    
    return f"{message} to {end}" if end else message


