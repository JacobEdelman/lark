from lark_utils import Fail
from terms import builtin_func, pattern_wild, expr, wild, seq, lit
from lexer import to_rules, lex
import string
class lark_int(int, expr):
    normal = True
    def match(self, x):
        if isinstance(x, lark_int) and self == x:
            return {}
        else:
            return Fail

    def __repr__(self):
        # super?
        return str(int(self))


class int_wild(wild): # just matches ints (subs for any...)
    lazy = False

    def match(self, x):
        if isinstance(x, lark_int) or isinstance(x, int_wild): # should include int_wild
            ret = {}
            ret[self.name] = x
            return ret
        else:
            return Fail
    def __repr__(self):
        return "int:"+self.name

def int_pattern_func(x):
    # this needs to bundle things methinks
    if (isinstance(x, seq) and all(isinstance(i, lit) for i in x)):
        # so... its getting passed a sequence...
        if isinstance(x,lit):
            str_val = x.val
        else:
            str_val = "".join(str(i.val) for i in x)

        if len(str_val) == 0:
            return Fail
        elif (len(str_val) == 1 or all(i in string.digits for i in str_val[1:])) and \
                (str_val[0] in string.digits+"-") and str_val!="-":
            return lark_int(str_val)
    return Fail

    # if isinstance(x, seq) and all(isinstance(i, lit) for i in x):
    #     x = "".join(x)


class int_pattern(pattern_wild):
    def __init__(self, name):
         self.pattern = int_pattern_func
         self.name = name



class addition_func(builtin_func):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.func = lambda matched_dict: lark_int(matched_dict[self.x]+matched_dict[self.y])
    def __repr__(self):
        return self.x.__repr__()+"+"+self.y.__repr__()

class subtraction_func(builtin_func):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.func = lambda matched_dict: lark_int(matched_dict[self.x]-matched_dict[self.y])
    def __repr__(self):
        return self.x.__repr__()+"-"+self.y.__repr__()
lark_true = lex("True")
lark_false = lex("False")
class less_than_func(builtin_func):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.func = lambda matched_dict: (matched_dict[self.x]<matched_dict[self.y] and lark_true ) or lark_false
    def __repr__(self):
        return self.x.__repr__()+"<"+self.y.__repr__()

class more_than_func(builtin_func):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.func = lambda matched_dict: (matched_dict[self.x]>matched_dict[self.y] and lark_true ) or lark_false
    def __repr__(self):
        return self.x.__repr__()+">"+self.y.__repr__()

class equal_func(builtin_func): # WILL NOT WORK
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.func = lambda matched_dict: (matched_dict[self.x]==matched_dict[self.y] and lark_true ) or lark_false
    def __repr__(self):
        return self.x.__repr__()+"=="+self.y.__repr__()

class mod_func(builtin_func): # WILL NOT WORK
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.func = lambda matched_dict: lark_int(matched_dict[self.x]%matched_dict[self.y])
    def __repr__(self):
        return self.x.__repr__()+"%"+self.y.__repr__()

int_cast_rule = (int_pattern("x"), int_pattern("x")) # so...
# int_wild_rule = (seq([int_wild("x")]), seq([int_wild("x")]))
# int_cast_rule2 = (int_pattern("x"), int_pattern("x"))
int_addition_rule = (seq([int_wild("x"), lit("+"), int_wild("y")]), addition_func("x", "y"))
int_subtraction_rule = (seq([int_wild("x"), lit("-"), int_wild("y")]), subtraction_func("x", "y"))
int_less_than_rule = (seq([int_wild("x"), lit("<"), int_wild("y")]), less_than_func("x", "y"))
int_more_than_rule = (seq([int_wild("x"), lit(">"), int_wild("y")]), more_than_func("x", "y"))
int_equals_rule = (seq([int_wild("x"), lit("is"), int_wild("y")]), equal_func("x", "y"))
int_mod_rule = (seq([int_wild("x"), lit("%"), int_wild("y")]), mod_func("x", "y"))
base_int_rules = [int_cast_rule, int_equals_rule, int_addition_rule, int_subtraction_rule,
    int_less_than_rule, int_more_than_rule, int_mod_rule]

gen_int_rules = to_rules("""
$x is $y = $x is $y
$x + $y = $x + $y
$x < $y = $x < $y
$x > $y = $x > $y
$x - $y = $x - $y
$x % $y = $x % $y""")
int_rules = base_int_rules + gen_int_rules
