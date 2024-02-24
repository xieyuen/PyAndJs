import asyncio

from java_script.micro_task.micro_task_queue import MicroTaskQueue


def run(fn):
    async def _run():
        if asyncio.iscoroutinefunction(fn):
            await fn()
        elif asyncio.iscoroutine(fn):
            await fn
        else:
            fn()

        await MicroTaskQueue.run()

    asyncio.run(_run())
