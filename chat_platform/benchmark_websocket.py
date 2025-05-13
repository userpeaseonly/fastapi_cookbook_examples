import uvicorn
import asyncio
from app.main import app

def run_server():
    """
    Run the FastAPI server with Uvicorn.
    """
    uvicorn.run(app)


from websockets import connect
async def connect_client(
    n: int, n_messages: int = 3
):
    async with connect(
        f"ws://localhost:8000/chatroom/user{n}",
    ) as client:
        for _ in range(n_messages):
            await client.send(
                f"Hello World from user{n}"
            )
            await asyncio.sleep(n * 0.1)
        await asyncio.sleep(2)

import multiprocessing
async def main(n_clients: int = 1000):
    p = multiprocessing.Process(target=run_server)
    p.start()
    await asyncio.sleep(1)
    connections = [
        connect_client(n) for n in range(n_clients)
    ]
    await asyncio.gather(*connections)
    await asyncio.sleep(1)
    p.terminate()

if __name__ == "__main__":
    asyncio.run(main())