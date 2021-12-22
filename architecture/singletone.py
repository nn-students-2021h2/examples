"""Test singleton"""

# pylint: disable=missing-function-docstring, missing-class-docstring, too-few-public-methods


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
    func2(1)
    func2(2)
    func2.foo = 3
    func2(4)

    _test_singleton(SingleInit)
    _test_singleton(SingleState)
    _test_singleton(SingleMeta)

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
examples>python singletone.py
func: 1
func: 1
func: 3
func2: 1
func2: 1
func2: 3

SingleInit: init
<class '__main__.SingleInit'>_1.foo: <__main__.SingleInit object at 0x000001EA0AB21BE0> foo
<class '__main__.SingleInit'>_1.foo: <__main__.SingleInit object at 0x000001EA0AB21BE0> 1
SingleInit: init
<class '__main__.SingleInit'>_2.foo: <__main__.SingleInit object at 0x000001EA0AB21BE0> 1

SingleState: init
<class '__main__.SingleState'>_1.foo: <__main__.SingleState object at 0x000001EA0AB21C10> foo
<class '__main__.SingleState'>_1.foo: <__main__.SingleState object at 0x000001EA0AB21C10> 1
SingleState: init
<class '__main__.SingleState'>_2.foo: <__main__.SingleState object at 0x000001EA0AB21C40> 1

SingleMeta: init
<class '__main__.SingleMeta'>_1.foo: <__main__.SingleMeta object at 0x000001EA0AB21C10> foo
<class '__main__.SingleMeta'>_1.foo: <__main__.SingleMeta object at 0x000001EA0AB21C10> 1
<class '__main__.SingleMeta'>_2.foo: <__main__.SingleMeta object at 0x000001EA0AB21C10> 1

SingleFactory: init
<class '__main__.SingleFactory'>_1.foo: <__main__.SingleFactory object at 0x000001EA0AB21C40> foo
<class '__main__.SingleFactory'>_1.foo: <__main__.SingleFactory object at 0x000001EA0AB21C40> 1
SingleFactory: init
<class '__main__.SingleFactory'>_2.foo: <__main__.SingleFactory object at 0x000001EA0AB21CD0> foo

<class '__main__.StaticClass'>_1.foo: <__main__.StaticClass object at 0x000001EA0AB21CD0> <bound method StaticClass.foo of <class '__main__.StaticClass'>>
<class '__main__.StaticClass'>_1.foo: <__main__.StaticClass object at 0x000001EA0AB21CD0> 1
<class '__main__.StaticClass'>_2.foo: <__main__.StaticClass object at 0x000001EA0AB21C40> <bound method StaticClass.foo of <class '__main__.StaticClass'>>

SingleFactory: init
SingleFactory.foo: 1

StaticClass.foo: 1 <property object at 0x000001EA0AB2CE50>
"""


r"""
"examples\singletone.py"
pylint
************* Module singletone
examples\singletone.py:120:4: E0213: Method should have "self" as first argument (no-self-argument)
************* Module singletone
examples\singletone.py:208:0: C0301: Line too long (120/100) (line-too-long)
examples\singletone.py:229:0: C0301: Line too long (120/100) (line-too-long)
examples\singletone.py:230:0: C0301: Line too long (128/100) (line-too-long)
examples\singletone.py:231:0: C0301: Line too long (117/100) (line-too-long)
examples\singletone.py:232:0: C0301: Line too long (117/100) (line-too-long)
examples\singletone.py:40:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:44:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:57:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:61:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:61:4: R0201: Method could be a function (no-self-use)
examples\singletone.py:80:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:84:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:103:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:107:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:116:4: C0104: Disallowed name "foo" (disallowed-name)
examples\singletone.py:120:4: E0213: Method should have "self" as first argument (no-self-argument)
examples\singletone.py:154:4: W0212: Access to a protected member _foo of a client class (protected-access)
examples\singletone.py:161:0: W0105: String statement has no effect (pointless-string-statement)
examples\singletone.py:204:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 7.70/10 (previous run: 7.30/10, +0.40)

Exit code: 30
Press any key to continue . . .
"""


r"""
mypy
examples\singletone.py:16: error: "Callable[[Any], Any]" has no attribute "foo"
examples\singletone.py:66: error: Need type annotation for '_instances' (hint: "_instances: Dict[<type>, <type>] = ...")
Found 2 errors in 1 file (checked 1 source file)
Press any key to continue . . .
"""
