from typing import NoReturn


def curry(fn):
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= fn.__code__.co_argcount:
            return fn(*args, **kwargs)
        else:
            return (
                lambda *more_args, **more_kwargs:
                curried(*args, *more_args, **kwargs, **more_kwargs)
            )

    return curried


def throw(err) -> NoReturn:
    if not isinstance(err, Exception):
        raise Exception(err)
    elif issubclass(err, Exception):
        raise err()
    raise err
