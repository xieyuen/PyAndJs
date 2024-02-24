from java_script import run
from java_script.micro_task import runMicroTask


def main():
    tid1 = runMicroTask(lambda: print("Hello"))
    tid2 = runMicroTask(lambda: print("World"))
    print(tid1, tid2, sep='\n')


if __name__ == '__main__':
    run(main)
