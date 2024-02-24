import asyncio


class MicroTask:
    def __init__(self, fn, *args, **kwargs):
        if not callable(fn):
            raise ValueError("Only callable objects can be run in MicroTaskQueue")

        self.__fn = fn
        self.__args = args
        self.__kwargs = kwargs

    async def run(self):
        if asyncio.iscoroutinefunction(self.__fn):
            asyncio.create_task(self.__fn(*self.__args, **self.__kwargs))
        else:
            async def fn():
                self.__fn(*self.__args, **self.__kwargs)

            asyncio.create_task(fn())
