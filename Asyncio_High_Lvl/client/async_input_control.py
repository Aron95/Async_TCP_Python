import asyncio
import async_input as ai


async def input_control():
    while True:
        try:
            i = await asyncio.create_task(ai.loop_for_input())
            p = int(i)
        except ValueError:
            print('Valid number, please')
            continue
        if 5000 <= p <= 8000:
            return p
        else:
            print("please choose a number between 5000 and 8000")
            continue
