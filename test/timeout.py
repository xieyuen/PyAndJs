from java_script.api.builtins import setTimeout


def test_setTimeout():
    def fn():
        print("setTimeout 异步执行")

    setTimeout(fn, 1000)

    print("同步执行")


if __name__ == '__main__':
    test_setTimeout()
