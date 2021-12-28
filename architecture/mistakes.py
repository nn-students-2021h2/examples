"""Test mistakes"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

import timeit


# LEGB Rule
# - Local (or function) scope
# - Enclosing (or nonlocal) scope
# - Global (or module) scope
# - Built-in scope

GLOBAL_VAR1 = []
GLOBAL_VAR2 = 1


def func_legb(param: list):
    GLOBAL_VAR1.append(1)
    GLOBAL_VAR2 = 2

    param += [1]
    print("func_legb param:", param)

    param = param + [2]
    print("func_legb param:", param)

    local_var = 1

    def embedded_func_legb():
        local_var = 2
        print("embedded_func_legb local_var:", local_var)

    embedded_func_legb()
    print("func_legb local_var:", local_var)


def legb_test():
    param = [0]
    func_legb(param)
    print("param:", param)
    print("GLOBAL_VAR1:", GLOBAL_VAR1)
    print("GLOBAL_VAR2:", GLOBAL_VAR2)


class A:
    foo = 1


class B(A):
    pass


class C(A):
    pass


def abc_test():
    print("\nABC:", A.foo, B.foo, C.foo)
    B.foo = 2
    print("ABC:", A.foo, B.foo, C.foo)
    A.foo = 3
    print("ABC:", A.foo, B.foo, C.foo)


def func_default_arg1(foo=[]):
    foo.append("foo")
    return foo


def func_default_arg2(foo=None):
    if foo is None:
        foo = []
    foo.append("foo")
    return foo


def default_arg_test():
    for i in range(3):
        print(f"\nfunc_default_arg1 {i}:", func_default_arg1())
        print(f"func_default_arg2 {i}:", func_default_arg2())


def is_equal_test():
    for a, b in [([], []), ([1], [1])]:
        print(f"\nis_equal {a} == {b}:", a == b)
        print(f"is_equal {a} is {b}:", a is b)


def print_exec_time(func):
    def wrap(*arg, **kwarg):
        start_time = timeit.default_timer()
        func(*arg, **kwarg)
        exec_time = timeit.default_timer() - start_time
        print(func, arg, kwarg, "- exec time:", exec_time)

    return wrap


@print_exec_time
def if_is(foo):
    for _i in range(10 ** 7):
        if foo is None:
            pass


@print_exec_time
def if_equal(foo):
    for _i in range(10 ** 7):
        if foo == None:
            pass


@print_exec_time
def if_none(foo):
    for _i in range(10 ** 7):
        if foo:
            pass


def if_test():
    print()
    if_is(None)
    if_equal(None)
    if_none(None)

    print()
    if_is([])
    if_equal([])
    if_none([])


@print_exec_time
def func_str1(str_len):
    append_str = "q" * str_len
    ret_str = ""
    for _i in range(10 ** 4):
        ret_str += append_str
    return ret_str


@print_exec_time
def func_str2(str_len):
    append_str = "q" * str_len
    ret_str = []
    for _i in range(10 ** 4):
        ret_str.append(append_str)
    return "".join(ret_str)


def str_test():
    print()
    func_str1(10 ** 2)
    func_str2(10 ** 2)

    print()
    func_str1(10 ** 3)
    func_str2(10 ** 3)


def dict_key(key):
    try:
        print(f"dict_key({key}):", end=" ")
        print({key: 1})
    except Exception as exc:
        print(exc)


def dict_key_test():
    print()
    dict_key(1)
    dict_key("1")
    dict_key((1,))
    dict_key(True)
    dict_key([1])
    dict_key({1: 1})
    dict_key(dict_key_test)
    dict_key(A())
    dict_key(A)


def _test():
    """Test and debug"""
    legb_test()
    abc_test()
    default_arg_test()
    if_test()
    str_test()
    dict_key_test()


if __name__ == "__main__":
    _test()


r"""
>python mistakes.py
func_legb param: [0, 1]
func_legb param: [0, 1, 2]
embedded_func_legb local_var: 2
func_legb local_var: 1
param: [0, 1]
GLOBAL_VAR1: [1]
GLOBAL_VAR2: 1

ABC: 1 1 1
ABC: 1 2 1
ABC: 3 2 3

func_default_arg1 0: ['foo']
func_default_arg2 0: ['foo']

func_default_arg1 1: ['foo', 'foo']
func_default_arg2 1: ['foo']

func_default_arg1 2: ['foo', 'foo', 'foo']
func_default_arg2 2: ['foo']

<function if_is at 0x0000019CD38ABCA0> (None,) {} - exec time: 0.3528536
<function if_equal at 0x0000019CD38ABDC0> (None,) {} - exec time: 0.46298069999999997
<function if_none at 0x0000019CD38ABEE0> (None,) {} - exec time: 0.3462565000000001

<function if_is at 0x0000019CD38ABCA0> ([],) {} - exec time: 0.3941026000000001
<function if_equal at 0x0000019CD38ABDC0> ([],) {} - exec time: 0.48714579999999996
<function if_none at 0x0000019CD38ABEE0> ([],) {} - exec time: 0.34770999999999974

<function func_str1 at 0x0000019CD38CD0D0> (100,) {} - exec time: 0.005604799999999965
<function func_str2 at 0x0000019CD38CD1F0> (100,) {} - exec time: 0.0019881999999999955

<function func_str1 at 0x0000019CD38CD0D0> (1000,) {} - exec time: 3.9186127
<function func_str2 at 0x0000019CD38CD1F0> (1000,) {} - exec time: 0.004958799999999819

dict_key(1): {1: 1}
dict_key(1): {'1': 1}
dict_key((1,)): {(1,): 1}
dict_key(True): {True: 1}
dict_key([1]): unhashable type: 'list'
dict_key({1: 1}): unhashable type: 'dict'
dict_key(<function dict_key_test at 0x0000019CD38CD430>): {<function dict_key_test at 0x0000019CD38CD430>: 1}
dict_key(<__main__.A object at 0x0000019CD38CB220>): {<__main__.A object at 0x0000019CD38CB220>: 1}
dict_key(<class '__main__.A'>): {<class '__main__.A'>: 1}
"""


r"""
pylint
************* Module mistakes
examples\architecture\mistakes.py:257:0: C0301: Line too long (126/100) (line-too-long)
examples\architecture\mistakes.py:258:0: C0301: Line too long (132/100) (line-too-long)
examples\architecture\mistakes.py:260:0: C0301: Line too long (119/100) (line-too-long)
examples\architecture\mistakes.py:262:0: C0301: Line too long (119/100) (line-too-long)
examples\architecture\mistakes.py:263:0: C0301: Line too long (119/100) (line-too-long)
examples\architecture\mistakes.py:264:0: C0301: Line too long (111/100) (line-too-long)
examples\architecture\mistakes.py:269:0: C0301: Line too long (107/100) (line-too-long)
examples\architecture\mistakes.py:270:0: C0301: Line too long (107/100) (line-too-long)
examples\architecture\mistakes.py:271:0: C0301: Line too long (107/100) (line-too-long)
examples\architecture\mistakes.py:20:4: W0621: Redefining name 'GLOBAL_VAR2' from outer scope (line 15) (redefined-outer-name)
examples\architecture\mistakes.py:20:4: C0103: Variable name "GLOBAL_VAR2" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:20:4: W0612: Unused variable 'GLOBAL_VAR2' (unused-variable)
examples\architecture\mistakes.py:46:0: C0103: Class name "A" doesn't conform to PascalCase naming style (invalid-name)
examples\architecture\mistakes.py:47:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:50:0: C0103: Class name "B" doesn't conform to PascalCase naming style (invalid-name)
examples\architecture\mistakes.py:54:0: C0103: Class name "C" doesn't conform to PascalCase naming style (invalid-name)
examples\architecture\mistakes.py:66:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
examples\architecture\mistakes.py:66:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:71:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:85:8: C0103: Variable name "a" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:85:11: C0103: Variable name "b" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:101:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:108:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:110:11: C0121: Comparison 'foo == None' should be 'foo is None' (singleton-comparison)
examples\architecture\mistakes.py:115:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:165:11: W0703: Catching too general exception Exception (broad-except)
examples\architecture\mistakes.py:196:0: W0105: String statement has no effect (pointless-string-statement)
examples\architecture\mistakes.py:245:0: W0105: String statement has no effect (pointless-string-statement)
examples\architecture\mistakes.py:280:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 7.70/10 (previous run: 7.73/10, -0.04)

Exit code: 20
"""


r"""
mypy
Success: no issues found in 1 source file
"""
