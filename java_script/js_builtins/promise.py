import traceback
from abc import abstractmethod, ABC
from typing import Callable, Optional, Any, List, Literal

__all__ = ["Promise"]

from java_script.js_builtins.timeout import setTimeout


class States:
    PENDING = "pending"
    FULFILLED = "fulfilled"
    REJECTED = "rejected"
    TYPE = Literal["pending", "fulfilled", "rejected"]


class Handler:
    def __init__(
            self,
            on_fulfilled: Optional[Any],
            on_rejected: Optional[Any],
            resolve: Callable[[Optional[Any]], None],
            reject: Callable[[Optional[Any]], None],
    ):
        self.on_fulfilled = on_fulfilled
        self.on_rejected = on_rejected
        self.resolve = resolve
        self.reject = reject


class PromiseLike(ABC):
    @abstractmethod
    def __init__(self, executor: Callable[[Callable, Callable], None]):
        raise NotImplementedError

    @abstractmethod
    def then(
            self,
            on_fulfilled: Optional[Callable[[Any], None]],
            on_rejected: Optional[Callable[[Any], None]]
    ) -> "Promise":
        raise NotImplementedError

    @staticmethod
    def isPromiseLike(v):
        """
        判断一个对象是否满足 Promise A+ 规范
        :param v:
        :return:
        """
        return v and hasattr(v, "then") and callable(v.then)

    @staticmethod
    def isThenable(v):
        """
        判断一个对象是否满足 Promise A+ 规范
        :param v:
        :return:
        """
        return PromiseLike.isPromiseLike(v)


class Promise(PromiseLike):

    def __init__(self, executor):
        """
        JavaScript Promise 类
        :param executor:
        """
        self.__state = States.PENDING
        self.__result = None  # type: Any
        self.__handlers = []  # type: List[Handler]

        try:
            executor(self.__exec_resolve, self.__exec__reject)
        except Exception as err:
            traceback.print_exc()
            self.__exec__reject(err)

    def __exec_resolve(self, data):
        self.__change_state(States.FULFILLED, data)

    def __exec__reject(self, data):
        self.__change_state(States.REJECTED, data)

    def __change_state(self, state, result):
        if self.__state != States.PENDING:
            return
        self.__state = state
        self.__result = result
        self.__run()

    def then(
            self,
            on_fulfilled: Optional[Callable[[Any], None]] = None,
            on_rejected: Optional[Callable[[type(Exception)], None]] = None
    ):
        """

        :param on_fulfilled:
        :param on_rejected:
        :return:
        """

        def executor(resolve, reject):
            self.__handlers.append(
                Handler(
                    on_fulfilled,
                    on_rejected,
                    resolve,
                    reject
                )
            )

            self.__run()

        return Promise(executor)

    def __run(self):
        if self.__state == States.PENDING:
            return
        if not self.__handlers:
            return
        for handler in self.__handlers:
            if self.__state == States.FULFILLED:
                self.__run_one(handler.on_fulfilled, handler.resolve, handler.reject)
            else:
                self.__run_one(handler.on_rejected, handler.resolve, handler.reject)
        self.__handlers.clear()

    def __run_one(self, callback, resolve, reject):
        def wrapper():
            if not callable(callback):
                fn = resolve if self.__state == States.FULFILLED else reject
                fn(self.__result)
                return

            try:
                ret = callback(self.__result)
                if self.isPromiseLike(ret):
                    ret.then(resolve, reject)
                else:
                    resolve(ret)
            except Exception as err:
                reject(err)

        setTimeout(wrapper, 0)

    def finally_(self, on_finally):
        """
        JavaScript Promise.prototype.finally 方法
        :param on_finally:
        :return:
        """

        def on_fulfilled(r):
            on_finally()
            return r

        def on_rejected(r):
            on_finally()
            raise Exception(r)

        return self.then(on_fulfilled, on_rejected)

    def catch(self, on_rejected):
        """
        JavaScript Promise.prototype.catch 方法
        :param on_rejected:
        :return:
        """
        return self.then(None, on_rejected)

    @staticmethod
    def resolve(v):
        if isinstance(v, Promise):
            return v

        @Promise
        def prom(resolve: Callable, reject: Callable):
            if PromiseLike.isPromiseLike(v):
                v.then(resolve, reject)
            else:
                resolve(v)

        return prom

    @staticmethod
    def reject(v):
        return Promise(lambda resolve, reject: reject(v))

    @staticmethod
    def all(promises):
        """
        JavaScript Promise.all 方法
        :param promises:
        :return:
        """
        length = len(promises)

        @Promise
        def prom(resolve, reject):
            if length == 0:
                resolve([])

            result = [None] * length
            fulfilledCount = 0

            def on_fulfilled(index, data):
                nonlocal fulfilledCount
                result[index] = data
                fulfilledCount += 1
                if fulfilledCount == length:
                    resolve(result)

            for i, p in enumerate(promises):
                Promise.resolve(p).then(
                    lambda data: on_fulfilled(i, data),
                    reject
                )

        return prom
