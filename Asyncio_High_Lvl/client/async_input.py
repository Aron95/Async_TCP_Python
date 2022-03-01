import asyncio
from concurrent.futures import ThreadPoolExecutor


# puts input() into an executor to make the input() function awaitable for asyncio
async def asyncInput():
    with ThreadPoolExecutor(1, 'Async Input') as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input)

# task for input() to add to the event loop


async def loop_for_input():
    while True:
        i = await asyncInput()
        return i
