import asyncio

import aiojobs



async def schedule():
    scheduler = await aiojobs.create_scheduler()
    await scheduler.spawn(coro(i / 10))
    # gracefully close spawned jobs
    await scheduler.close()
    asyncio.get_event_loop().run_until_complete(schedule())
