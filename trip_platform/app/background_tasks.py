import asyncio
import logging

logger = logging.getLogger("uvicorn.error")


async def store_query_to_external_db(message: str):
    """
    Simulate storing a message to an external database.
    """
    logger.info(f"Storing message to external DB: {message}")
    await asyncio.sleep(1)  # Simulate a network delay
    logger.info("Message stored successfully.")