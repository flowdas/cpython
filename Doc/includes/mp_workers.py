import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

#
# 작업자 프로세스가 실행하는 함수
#

def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

#
# 결과를 계산하는데 사용되는 함수
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# 작업이 참조하는 함수
#

def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b

#
#
#

def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(mul, (i, 7)) for i in range(20)]
    TASKS2 = [(plus, (i, 8)) for i in range(10)]

    # 큐를 만듭니다
    task_queue = Queue()
    done_queue = Queue()

    # 작업을 제출합니다
    for task in TASKS1:
        task_queue.put(task)

    # 작업자 프로세스를 시작합니다
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # 결과를 갖고와서 인쇄합니다
    print('순서없는 결과:')
    for i in range(len(TASKS1)):
        print('\t', done_queue.get())

    # `put()` 을 사용해서 작업을 추가합니다
    for task in TASKS2:
        task_queue.put(task)

    # 결과를 더 갖고와서 인쇄합니다
    for i in range(len(TASKS2)):
        print('\t', done_queue.get())

    # 자식 프로세스에게 정지하라고 알립니다
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    freeze_support()
    test()
