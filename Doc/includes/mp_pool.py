import multiprocessing
import time
import random
import sys

#
# 테스트 코드가 사용하는 함수
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % (
        multiprocessing.current_process().name,
        func.__name__, args, result
        )

def calculatestar(args):
    return calculate(*args)

def mul(a, b):
    time.sleep(0.5 * random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5 * random.random())
    return a + b

def f(x):
    return 1.0 / (x - 5.0)

def pow3(x):
    return x ** 3

def noop(x):
    pass

#
# 테스트 코드
#

def test():
    PROCESSES = 4
    print('%d 프로세스로 풀을 만듭니다\n' % PROCESSES)

    with multiprocessing.Pool(PROCESSES) as pool:
        #
        # 테스트
        #

        TASKS = [(mul, (i, 7)) for i in range(10)] + \
                [(plus, (i, 8)) for i in range(10)]

        results = [pool.apply_async(calculate, t) for t in TASKS]
        imap_it = pool.imap(calculatestar, TASKS)
        imap_unordered_it = pool.imap_unordered(calculatestar, TASKS)

        print('pool.apply_async() 를 사용한 순서있는 결과:')
        for r in results:
            print('\t', r.get())
        print()

        print('pool.imap() 를 사용한 순서있는 결과:')
        for x in imap_it:
            print('\t', x)
        print()

        print('pool.imap_unordered() 를 사용한 순서없는 결과:')
        for x in imap_unordered_it:
            print('\t', x)
        print()

        print('pool.map() 를 사용한 순서있는 결과 --- 완료할 때까지 블록합니다:')
        for x in pool.map(calculatestar, TASKS):
            print('\t', x)
        print()

        #
        # 에러 처리 테스트
        #

        print('에러 처리를 검사합니다:')

        try:
            print(pool.apply(f, (5,)))
        except ZeroDivisionError:
            print('\tpool.apply() 로 부터 기대한 ZeroDivisionError 를 받았습니다')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(pool.map(f, list(range(10))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from pool.map()')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(list(pool.imap(f, list(range(10)))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from list(pool.imap())')
        else:
            raise AssertionError('expected ZeroDivisionError')

        it = pool.imap(f, list(range(10)))
        for i in range(10):
            try:
                x = next(it)
            except ZeroDivisionError:
                if i == 5:
                    pass
            except StopIteration:
                break
            else:
                if i == 5:
                    raise AssertionError('expected ZeroDivisionError')

        assert i == 9
        print('\tGot ZeroDivisionError as expected from IMapIterator.next()')
        print()

        #
        # 시간 제한 테스트
        #

        print('Testing ApplyResult.get() with timeout:', end=' ')
        res = pool.apply_async(calculate, TASKS[0])
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % res.get(0.02))
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()

        print('Testing IMapIterator.next() with timeout:', end=' ')
        it = pool.imap(calculatestar, TASKS)
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % it.next(0.02))
            except StopIteration:
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test()
