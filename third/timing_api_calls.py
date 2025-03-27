import uvicorn
from main import app
import asyncio
from httpx import AsyncClient
import time

def run_server():
    uvicorn.run(app, host="8000", log_level="error")



from contextlib import contextmanager
from multiprocessing import Process
@contextmanager
def run_server_in_process():
    p = Process(target=run_server)
    p.start()
    time.sleep(2)  # Give the server a second to start
    print("Server is running in a separate process")
    yield
    p.terminate()



async def make_requests_to_the_endpoint(
    n: int, path: str
):
    async with AsyncClient(
        base_url="http://localhost:8000"
    ) as client:
        tasks = (
            client.get(path, timeout=float("inf"))
            for _ in range(n)
        )
        await asyncio.gather(*tasks)
    

async def main(n: int = 10):
    with run_server_in_process():
        begin = time.time()
        await make_requests_to_the_endpoint(n,
                                            "/sync")
        end = time.time()
        print(
            f"Time taken to make {n} requests "
            f"to sync endpoint: {end - begin} seconds"
        )
        begin = time.time()
        await make_requests_to_the_endpoint(n,
                                            "/async")
        end = time.time()
        print(
            f"Time taken to make {n} requests "
            f"to async endpoint: {end - begin} seconds"
        )


if __name__ == "__main__":
    asyncio.run(main(n=100))