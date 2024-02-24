import asyncio
from typing import Dict

from java_script.micro_task.micro_task import MicroTask


class MicroTaskQueue:
    __tasks: Dict[int, MicroTask] = {}

    @staticmethod
    def __generate_id(task):
        # 生成唯一的ID
        return id(task)

    @classmethod
    def add(cls, task: MicroTask):
        _id = cls.__generate_id(task)
        cls.__tasks[_id] = task
        return _id

    @classmethod
    def remove(cls, _id):
        del cls.__tasks[_id]

    @classmethod
    async def run(cls):
        for _id, task in cls.__tasks.items():
            asyncio.create_task(task.run())
        cls.__tasks.clear()
