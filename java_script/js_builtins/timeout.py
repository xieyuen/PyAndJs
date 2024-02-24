import time

from java_script.micro_task import runMicroTask

__all__ = ["setTimeout"]


class SetTimeoutDecResult:
    def __init__(self, fn, _id):
        self.__fn = fn
        self.id = _id

    def __call__(self, *args, **kwargs):
        return self.__fn(*args, **kwargs)

    def getFunction(self):
        return self.__fn


def setTimeout(fn, delay):
    """
        JavaScript setTimeout 实现
        返回任务 id
        :param fn:
        :param delay:
        :return:
        """

    def _task_callback():
        time.sleep(delay / 1000)
        fn()

    return runMicroTask(_task_callback)
