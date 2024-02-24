from java_script.micro_task.micro_task import MicroTask
from java_script.micro_task.micro_task_queue import MicroTaskQueue

__all__ = ["runMicroTask"]


def runMicroTask(fn, *args, **kwargs):
    """
    在微队列里运行微任务
    :param fn:
    :param args:
    :param kwargs:
    :return: 微任务的 id
    """
    task = MicroTask(fn, *args, **kwargs)
    _id = MicroTaskQueue.add(task)
    return _id


def cancelMicroTask(_id):
    """
    取消微任务
    :param _id:
    :return:
    """
    MicroTaskQueue.remove(_id)
