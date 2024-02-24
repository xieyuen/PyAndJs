from java_script.api.builtins import Promise


def on_fulfilled(value):
    print(value)


def main():
    proms = [Promise(lambda s, j: s(i)) for i in range(10)]
    resProm = Promise.all(proms)
    resProm.then(on_fulfilled)


if __name__ == '__main__':
    main()
