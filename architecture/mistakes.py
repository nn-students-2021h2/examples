"""Test mistakes"""

# pylint: disable=missing-function-docstring,missing-class-docstring,too-few-public-methods

import copy
import timeit


# LEGB Rule
# - Local (or function) scope
# - Enclosing (or nonlocal) scope
# - Global (or module) scope
# - Built-in scope

# https://docs.python.org/3.9/faq/programming.html#core-language


GLOBAL_VAR1 = []
GLOBAL_VAR2 = 1


def func_legb(param: list):
    GLOBAL_VAR1.append(1)
    GLOBAL_VAR2 = 2

    param += [1]
    print("func_legb param += [1]:", param)

    param = param + [2]
    print("func_legb param + [2]:", param)

    local_var = []

    def embedded_func_legb1():
        print("embedded_func_legb1 start local_var:", local_var)
        local_var.append(1)
        print("embedded_func_legb1 end local_var:", local_var)

    embedded_func_legb1()
    print("func_legb local_var:", local_var)

    def embedded_func_legb2():
        print("embedded_func_legb2 start local_var:", local_var)
        local_var += [2]
        print("embedded_func_legb2 end local_var:", local_var)

    # embedded_func_legb2()


#   Traceback (most recent call last):
#     File "mistakes.py", line 47, in func_legb
#       embedded_func_legb2()
#     File "mistakes.py", line 43, in embedded_func_legb2
#       print("embedded_func_legb2 start local_var:", local_var)
#   UnboundLocalError: local variable 'local_var' referenced before assignment


def legb_test():
    param = [0]
    func_legb(param)
    print("legb_test param:", param)
    print("GLOBAL_VAR1:", GLOBAL_VAR1)
    print("GLOBAL_VAR2:", GLOBAL_VAR2)


def mutable_test():
    print()
    a = [1]
    b = a
    b.append(2)
    print("mutable_test list a b:", a, b)

    x = 1
    y = x
    y += 1
    print("mutable_test int x y:", x, y)

    a = [1]
    b = a[:]  # a.copy()
    b.append(2)
    print("mutable_test list copy a b:", a, b)

    a = {1: [1]}
    b = a.copy()
    a[1].append(2)
    print("mutable_test dict copy a b:", a, b)

    a = {1: [1]}
    b = copy.deepcopy(a)
    a[1].append(2)
    print("mutable_test dict deepcopy a b:", a, b)


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
    mutable_test()
    abc_test()
    default_arg_test()
    is_equal_test()
    if_test()
    str_test()
    dict_key_test()


if __name__ == "__main__":
    _test()


# pylint: disable=line-too-long,pointless-string-statement

r"""
>python mistakes.py
func_legb param += [1]: [0, 1]
func_legb param + [2]: [0, 1, 2]
embedded_func_legb1 start local_var: []
embedded_func_legb1 end local_var: [1]
func_legb local_var: [1]
legb_test param: [0, 1]
GLOBAL_VAR1: [1]
GLOBAL_VAR2: 1

mutable_test list a b: [1, 2] [1, 2]
mutable_test int x y: 1 2
mutable_test list copy a b: [1] [1, 2]
mutable_test dict copy a b: {1: [1, 2]} {1: [1, 2]}
mutable_test dict deepcopy a b: {1: [1, 2]} {1: [1]}

ABC: 1 1 1
ABC: 1 2 1
ABC: 3 2 3

func_default_arg1 0: ['foo']
func_default_arg2 0: ['foo']

func_default_arg1 1: ['foo', 'foo']
func_default_arg2 1: ['foo']

func_default_arg1 2: ['foo', 'foo', 'foo']
func_default_arg2 2: ['foo']

is_equal [] == []: True
is_equal [] is []: False

is_equal [1] == [1]: True
is_equal [1] is [1]: False

<function if_is at 0x000001B3D4DDE0D0> (None,) {} - exec time: 0.3433525
<function if_equal at 0x000001B3D4DDE1F0> (None,) {} - exec time: 0.3669428
<function if_none at 0x000001B3D4DDE310> (None,) {} - exec time: 0.24501839999999997

<function if_is at 0x000001B3D4DDE0D0> ([],) {} - exec time: 0.31276669999999995
<function if_equal at 0x000001B3D4DDE1F0> ([],) {} - exec time: 0.3963250999999999
<function if_none at 0x000001B3D4DDE310> ([],) {} - exec time: 0.2756681000000001

<function func_str1 at 0x000001B3D4DDE4C0> (100,) {} - exec time: 0.0027449999999999974
<function func_str2 at 0x000001B3D4DDE5E0> (100,) {} - exec time: 0.0011468000000001144

<function func_str1 at 0x000001B3D4DDE4C0> (1000,) {} - exec time: 3.3518665000000003
<function func_str2 at 0x000001B3D4DDE5E0> (1000,) {} - exec time: 0.004182799999999709

dict_key(1): {1: 1}
dict_key(1): {'1': 1}
dict_key((1,)): {(1,): 1}
dict_key(True): {True: 1}
dict_key([1]): unhashable type: 'list'
dict_key({1: 1}): unhashable type: 'dict'
dict_key(<function dict_key_test at 0x000001B3D4DDE820>): {<function dict_key_test at 0x000001B3D4DDE820>: 1}
dict_key(<__main__.A object at 0x000001B3D4DCAFD0>): {<__main__.A object at 0x000001B3D4DCAFD0>: 1}
dict_key(<class '__main__.A'>): {<class '__main__.A'>: 1}
"""


r"""
pylint
************* Module mistakes
examples\architecture\mistakes.py:43:54: E0601: Using variable 'local_var' before assignment (used-before-assignment)
************* Module mistakes
examples\architecture\mistakes.py:24:4: W0621: Redefining name 'GLOBAL_VAR2' from outer scope (line 19) (redefined-outer-name)
examples\architecture\mistakes.py:24:4: C0103: Variable name "GLOBAL_VAR2" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:43:54: E0601: Using variable 'local_var' before assignment (used-before-assignment)
examples\architecture\mistakes.py:24:4: W0612: Unused variable 'GLOBAL_VAR2' (unused-variable)
examples\architecture\mistakes.py:42:4: W0612: Unused variable 'embedded_func_legb2' (unused-variable)
examples\architecture\mistakes.py:68:4: C0103: Variable name "a" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:69:4: C0103: Variable name "b" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:73:4: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:74:4: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:75:4: C0103: Variable name "y" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:78:4: C0103: Variable name "a" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:79:4: C0103: Variable name "b" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:83:4: C0103: Variable name "a" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:84:4: C0103: Variable name "b" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:88:4: C0103: Variable name "a" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:89:4: C0103: Variable name "b" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:94:0: C0103: Class name "A" doesn't conform to PascalCase naming style (invalid-name)
examples\architecture\mistakes.py:95:4: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:98:0: C0103: Class name "B" doesn't conform to PascalCase naming style (invalid-name)
examples\architecture\mistakes.py:102:0: C0103: Class name "C" doesn't conform to PascalCase naming style (invalid-name)
examples\architecture\mistakes.py:114:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
examples\architecture\mistakes.py:114:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:119:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:133:8: C0103: Variable name "a" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:133:11: C0103: Variable name "b" doesn't conform to snake_case naming style (invalid-name)
examples\architecture\mistakes.py:149:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:156:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:158:11: C0121: Comparison 'foo == None' should be 'foo is None' (singleton-comparison)
examples\architecture\mistakes.py:163:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:213:11: W0703: Catching too general exception Exception (broad-except)

------------------------------------------------------------------
Your code has been rated at 7.81/10 (previous run: 7.81/10, +0.00)

Exit code: 22
"""


r"""
mypy
examples\architecture\mistakes.py:32: error: Need type annotation for 'local_var' (hint: "local_var: List[<type>] = ...")
Found 1 error in 1 file (checked 1 source file)
"""
