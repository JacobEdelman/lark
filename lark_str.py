from lark_utils import Fail
from terms import builtin_func, pattern_wild, expr, wild, seq, lit
from lark_int import lark_int
from lexer import to_rules, lex
from ast import literal_eval # BAD
import string
# add in one item list
def str_pattern_func(x):
    if isinstance(x,lit) and x.val == '""': # shouldn't happen..
        return lex("str(nil)")
    elif isinstance(x,seq) and len(x) == 1 and isinstance(x[0], lit) and x[0].val[0] == '"' and x[0].val[-1] == '"':
        # No Check
        # if not all(i!= '"' for i in x[0].val[1:-1]):
        #     return Fail

        try:
            lit_val = literal_eval(x[0].val)
        except ValueError:
            return Fail

        items = lit_val[::-1]
        ret = lex("nil")
        #eval it for escaped stuffs
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


str_cast_rule = (str_pattern("x"), str_pattern("x"))
gen_str_rules = to_rules("""
char($a) = char($a)
str($a) = str($a)
""")
base_str_rules = [str_cast_rule]
str_rules = base_str_rules + gen_str_rules
