import logging
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")


logger = logging.getLogger("uvicorn.error")


async def ping_mongo_db_server():
    try:
        await mongo_client.admin.command("ping")
        logger.info("MongoDB server is reachable.")
    except Exception as e:
        logger.error(f"MongoDB server is not reachable: {e}")
        raise e


