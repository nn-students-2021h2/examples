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
    print()
    for _i in range(3):
        print("func_default_arg1:", func_default_arg1())
        print("func_default_arg2:", func_default_arg2())


def print_exec_time(func):
    def wrap(*arg, **kwarg):
        start_time = timeit.default_timer()
        func(*arg, **kwarg)
        print(func, "- exec time:", timeit.default_timer() - start_time)

    return wrap


@print_exec_time
def func_str1(foo):
    ret_str = ""
    for _i in range(10000):
        ret_str += foo
    return ret_str


@print_exec_time
def func_str2(foo):
    ret_str = []
    for _i in range(10000):
        ret_str.append(foo)
    return "".join(ret_str)


def str_test():
    print()
    func_str1("q" * 1000)
    func_str2("q" * 1000)


def _test():
    """Test and debug"""
    legb_test()
    abc_test()
    default_arg_test()
    str_test()


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

func_default_arg1: ['foo']
func_default_arg2: ['foo']
func_default_arg1: ['foo', 'foo']
func_default_arg2: ['foo']
func_default_arg1: ['foo', 'foo', 'foo']
func_default_arg2: ['foo']

<function func_str1 at 0x000002951FFDBC10> - exec time: 3.4818261
<function func_str2 at 0x000002951FFDBD30> - exec time: 0.004020099999999971
"""


r"""
pylint
************* Module mistakes
examples\architecture\mistakes.py:158:0: C0301: Line too long (126/100) (line-too-long)
examples\architecture\mistakes.py:159:0: C0301: Line too long (132/100) (line-too-long)
examples\architecture\mistakes.py:161:0: C0301: Line too long (119/100) (line-too-long)
examples\architecture\mistakes.py:163:0: C0301: Line too long (119/100) (line-too-long)
examples\architecture\mistakes.py:164:0: C0301: Line too long (119/100) (line-too-long)
examples\architecture\mistakes.py:165:0: C0301: Line too long (111/100) (line-too-long)
examples\architecture\mistakes.py:170:0: C0301: Line too long (107/100) (line-too-long)
examples\architecture\mistakes.py:171:0: C0301: Line too long (107/100) (line-too-long)
examples\architecture\mistakes.py:172:0: C0301: Line too long (107/100) (line-too-long)
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
examples\architecture\mistakes.py:95:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:103:0: C0104: Disallowed name "foo" (disallowed-name)
examples\architecture\mistakes.py:128:0: W0105: String statement has no effect (pointless-string-statement)
examples\architecture\mistakes.py:154:0: W0105: String statement has no effect (pointless-string-statement)
examples\architecture\mistakes.py:181:0: W0105: String statement has no effect (pointless-string-statement)

------------------------------------------------------------------
Your code has been rated at 6.88/10 (previous run: 6.88/10, +0.00)

Exit code: 20
"""


r"""
mypy
Success: no issues found in 1 source file
"""
