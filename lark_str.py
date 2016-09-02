from lark_utils import Fail, flatten
from terms import builtin_func, pattern_wild, expr, wild, seq, lit
from lark_int import lark_int, int_wild
from lexer import to_rules, lex
from ast import literal_eval
import string

def str_pattern_func(x, exprs = None):
    if isinstance(x,lit) and x.val == '""':
        return lex("str(nil)")
    elif isinstance(x,seq) and len(x) == 1 and isinstance(x[0], lit) and x[0].val[0] == '"' and x[0].val[-1] == '"':

        try:
            lit_val = literal_eval(x[0].val)
        except ValueError:
            return Fail

        items = lit_val[::-1]
        ret = lex("nil")
        for i in items:
            ret = seq(
                    lex("cons(") +
                    seq([seq(lex("char(")+(lark_int(ord(i)),)+lex(")"))])+lex(",")+seq([ret])+lex(")"))
        return seq(lex("str(")+seq([ret])+lex(")"))
    else:
        return Fail

class str_pattern(pattern_wild):
    def __init__(self, name):
         self.pattern = str_pattern_func
         self.name = name
    memed = {}
    def parse(self, x, exprs):
        memed = self.memed
        if x in memed:
            return memed[x]
        memed[x] = self.pattern(x, exprs )
        return memed[x]
def to_lark_str(x):
    return str_pattern_func(lex('"'+x.__repr__()[1:-1].replace('"','\\"')+'"')) # WAT??
def str_val(x):
    if isinstance(x, seq) and len(x) == 4 and isinstance(x[0], lit) and \
        isinstance(x[1], lit) and x[0].val == "str" and x[1].val == "(" and \
        isinstance(x[2], seq) and isinstance(x[3], lit) and x[3].val == ")":
        test = str_val_helper(x[2])
        if test != None:
            return test
    return flatten(x)

def str_val_helper(x):
    if isinstance(x, seq) and len(x) == 1 and isinstance(x[0], lit) and \
        x[0].val == "nil":
        return ""
    elif not isinstance(x, seq) or len(x) != 6 or not isinstance(x[2], seq)\
        or len(x[2]) != 4:
        return None
    test = str_val_helper(x[-2])
    if test == None:
        return None
    return chr(x[2][2]) + test

class int_to_str_func(builtin_func):
    def __init__(self, x):
        self.x = x
        self.func = lambda matched_dict: to_lark_str(str(matched_dict[self.x]))
    def __repr__(self):
        return "str(" + self.x.__repr__() + ")"



str_cast_rule = (str_pattern("x"), str_pattern("x"))
int_str_rule = (seq([lit("str"), lit("("), int_wild("x"), lit(")")]), int_to_str_func("x"))
gen_str_rules = to_rules("""
char($a) = char($a)
str($a) = str($a)
str(str($x)) = str($x)
""")
base_str_rules = [str_cast_rule, int_str_rule]
str_rules = base_str_rules + gen_str_rules
