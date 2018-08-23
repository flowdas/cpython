from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager, BaseProxy
import operator

##

class Foo:
    def f(self):
        print('Foo.f() 를 호출했습니다')
    def g(self):
        print('Foo.g() 를 호출했습니다')
    def _h(self):
        print('Foo._h() 를 호출했습니다')

# 간단한 제너레이터 함수
def baz():
    for i in range(10):
        yield i*i

# 제너레이터 객체의 프락시 형
class GeneratorProxy(BaseProxy):
    _exposed_ = ['__next__']
    def __iter__(self):
        return self
    def __next__(self):
        return self._callmethod('__next__')

# operator 모듈을 반환하는 함수
def get_operator_module():
    return operator

##

class MyManager(BaseManager):
    pass

# Foo 클래스를 등록합니다; 프락시가 `f()` 와 `g()` 에 접근할 수 있게 합니다
MyManager.register('Foo1', Foo)

# Foo 클래스를 등록합니다; 프락시가 `g()` 와 `_h()` 에 접근할 수 있게 합니다
MyManager.register('Foo2', Foo, exposed=('g', '_h'))

# 제너레이터 함수 baz 를 등록합니다; 프락시를 만드는데 `GeneratorProxy` 를 사용합니다
MyManager.register('baz', baz, proxytype=GeneratorProxy)

# get_operator_module() 를 등록합니다; 프락시가 공개 함수에 접근할 수 있게 합니다
MyManager.register('operator', get_operator_module)

##

def test():
    manager = MyManager()
    manager.start()

    print('-' * 20)

    f1 = manager.Foo1()
    f1.f()
    f1.g()
    assert not hasattr(f1, '_h')
    assert sorted(f1._exposed_) == sorted(['f', 'g'])

    print('-' * 20)

    f2 = manager.Foo2()
    f2.g()
    f2._h()
    assert not hasattr(f2, 'f')
    assert sorted(f2._exposed_) == sorted(['g', '_h'])

    print('-' * 20)

    it = manager.baz()
    for i in it:
        print('<%d>' % i, end=' ')
    print()

    print('-' * 20)

    op = manager.operator()
    print('op.add(23, 45) =', op.add(23, 45))
    print('op.pow(2, 94) =', op.pow(2, 94))
    print('op._exposed_ =', op._exposed_)

##

if __name__ == '__main__':
    freeze_support()
    test()
