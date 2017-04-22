import asyncio
from concurrent.futures import ProcessPoolExecutor

async def async_wrapper(loop, *args):
    await loop.run_in_executor(ProcessPoolExecutor(), *args)