"""Test singleton"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods


def func(param):
    try:
        func.foo
    except AttributeError:
        func.foo = param
    print("func:", func.foo)


func(1)
func(2)
func.foo = 3
func(4)


def func2(param):
    if not hasattr(func2, "foo"):
        func2.foo = param
    print("func2:", func2.foo)


class SingleVar:
    def __init__(self, foo_value=None):
        print("SingleVar: init")
        self._foo = foo_value or "foo"

    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value):
        self._foo = value


SINGLE_VAR = SingleVar()

SINGLE_VAR.foo = 1
print("SingleVar.foo:", SINGLE_VAR, SINGLE_VAR.foo)


class SingleInit:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingleInit, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, foo_value=None):
        print("SingleInit: init")
        if not hasattr(self, "_foo"):
            self._foo = foo_value or "foo"

    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value):
        self._foo = value


class SingleState:
    _foo = None

    def __init__(self, foo_value=None):
        print("SingleState: init")
        if SingleState._foo is None:
            SingleState._foo = foo_value or "foo"

    @property
    def foo(self):
        return SingleState._foo

    @foo.setter
    def foo(self, value):
        SingleState._foo = value


# Auto-magically covers inheritances
class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingleMeta(metaclass=MetaSingleton):
    def __init__(self, foo_value=None):
        print("SingleMeta: init")
        self._foo = foo_value or "foo"

    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value):
        self._foo = value


def singleton_decor(class_def):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_def not in instances:
            instances[class_def] = class_def(*args, **kwargs)
        return instances[class_def]

    return get_instance


# It is a function (not a class), so you cannot call class methods from it
@singleton_decor
class SingleDecor:
    def __init__(self, foo_value=None):
        print("SingleDecor: init")
        self._foo = foo_value or "foo"

    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value):
        self._foo = value


class SingleFactory:
    _instance = None

    def __init__(self, foo_value=None):
        print("SingleFactory: init")
        if not SingleFactory._instance:
            self._foo = foo_value or "foo"

    @classmethod
    def get_instance(cls, foo_value=None):
        if not cls._instance:
            cls._instance = SingleFactory(foo_value)
        return cls._instance

    @property
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value):
        self._foo = value


class StaticClass:
    # foo = "foo"
    _foo = "foo"

    @classmethod
    def foo(cls):
        return cls._foo

    # Mistake
    @property
    def foo_prop(cls):
        return cls._foo


def _test_singleton(class_def):
    print()
    obj_1 = class_def()
    print(f"{class_def}_1.foo:", obj_1, obj_1.foo)
    obj_1.foo = 1
    print(f"{class_def}_1.foo:", obj_1, obj_1.foo)
    obj_2 = class_def()
    print(f"{class_def}_2.foo:", obj_2, obj_2.foo)


def _test():
    """Test and debug"""
    print()

    func2(1)
    func2(2)
    func2.foo = 3
    func2(4)

    _test_singleton(SingleInit)
    _test_singleton(SingleState)
    _test_singleton(SingleMeta)
    _test_singleton(SingleDecor)

    # Wrong
    _test_singleton(SingleFactory)
    _test_singleton(StaticClass)

    print()
    SingleFactory.get_instance().foo = 1
    print("SingleFactory.foo:", SingleFactory.get_instance().foo)

    print()
    StaticClass._foo = 1
    print("StaticClass.foo:", StaticClass.foo(), StaticClass.foo_prop)


if __name__ == "__main__":
    _test()


r"""
>python singletone.py
func: 1
func: 1
func: 3
SingleVar: init
SingleVar.foo: <__main__.SingleVar object at 0x00000201E40028E0> 1

func2: 1
func2: 1
func2: 3

SingleInit: init
<class '__main__.SingleInit'>_1.foo: <__main__.SingleInit object at 0x00000201E4521D00> foo
<class '__main__.SingleInit'>_1.foo: <__main__.SingleInit object at 0x00000201E4521D00> 1
SingleInit: init
<class '__main__.SingleInit'>_2.foo: <__main__.SingleInit object at 0x00000201E4521D00> 1

SingleState: init
<class '__main__.SingleState'>_1.foo: <__main__.SingleState object at 0x00000201E4547070> foo
<class '__main__.SingleState'>_1.foo: <__main__.SingleState object at 0x00000201E4547070> 1
SingleState: init
<class '__main__.SingleState'>_2.foo: <__main__.SingleState object at 0x00000201E45470A0> 1

SingleMeta: init
<class '__main__.SingleMeta'>_1.foo: <__main__.SingleMeta object at 0x00000201E4547070> foo
<class '__main__.SingleMeta'>_1.foo: <__main__.SingleMeta object at 0x00000201E4547070> 1
<class '__main__.SingleMeta'>_2.foo: <__main__.SingleMeta object at 0x00000201E4547070> 1

SingleDecor: init
<function singleton_decor.<locals>.get_instance at 0x00000201E452BC10>_1.foo: <__main__.SingleDecor object at 0x00000201E45470A0> foo
<function singleton_decor.<locals>.get_instance at 0x00000201E452BC10>_1.foo: <__main__.SingleDecor object at 0x00000201E45470A0> 1
<function singleton_decor.<locals>.get_instance at 0x00000201E452BC10>_2.foo: <__main__.SingleDecor object at 0x00000201E45470A0> 1

SingleFactory: init
<class '__main__.SingleFactory'>_1.foo: <__main__.SingleFactory object at 0x00000201E4547130> foo
<class '__main__.SingleFactory'>_1.foo: <__main__.SingleFactory object at 0x00000201E4547130> 1
SingleFactory: init
<class '__main__.SingleFactory'>_2.foo: <__main__.SingleFactory object at 0x00000201E4547190> foo

<class '__main__.StaticClass'>_1.foo: <__main__.StaticClass object at 0x00000201E4547190> <bound method StaticClass.foo of <class '__main__.StaticClass'>>
<class '__main__.StaticClass'>_1.foo: <__main__.StaticClass object at 0x00000201E4547190> 1
<class '__main__.StaticClass'>_2.foo: <__main__.StaticClass object at 0x00000201E4547130> <bound method StaticClass.foo of <class '__main__.StaticClass'>>

SingleFactory: init
SingleFactory.foo: 1

StaticClass.foo: 1 <property object at 0x00000201E4530220>
"""


r"""
pylint
************* Module singletone
examples\architecture\singletone.py:169:4: E0213: Method should have "self" as first argument (no-self-argument)
************* Module singletone
examples\architecture\singletone.py:271:0: C0301: Line too long (110/100) (line-too-long)
examples\architecture\singletone.py:272:0: C0301: Line too long (151/100) (line-too-long)
examples\architecture\singletone.py:42:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:32:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:36:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:60:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:64:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:77:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:81:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:81:4: R0201: Method could be a function (no-self-use)
examples\architecture\singletone.py:101:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:105:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:128:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:132:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:151:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:155:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:164:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\singletone.py:169:4: E0213: Method should have "self" as first argument (no-self-argument)
examples\architecture\singletone.py:206:4: W0212: Access to a protected member _foo of a client class (protected-access)
examples\architecture\singletone.py:213:0: W0105: String statement has no effect (pointless-string-statement)
examples\architecture\singletone.py:264:0: W0105: String statement has no effect (pointless-string-statement)
examples\architecture\singletone.py:269:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 7.98/10 (previous run: 7.70/10, +0.28)

Exit code: 30
"""


r"""
mypy
examples\architecture\singletone.py:16: error: "Callable[[Any], Any]" has no attribute "foo"
examples\architecture\singletone.py:87: error: Need type annotation for '_instances' (hint: "_instances: Dict[<type>, <type>] = ...")
Found 2 errors in 1 file (checked 1 source file)
"""
