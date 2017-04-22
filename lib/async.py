import asyncio
from concurrent.futures import ThreadPoolExecutor

async def async_wrapper(loop, *args, **kwargs):
    fn = args[0]
    real_args = args[1:]
    await loop.run_in_executor(ThreadPoolExecutor(), lambda: fn(*real_args, **kwargs))