from lark_utils import Fail
from terms import builtin_func, pattern_wild, expr, wild, seq, lit
from lexer import to_rules, lex
import string

def list_pattern_func(x):
    if isinstance(x,lit) and x.val == "()": # shouldn't happen..
        return lex("nil")
    elif isinstance(x,seq) and len(x)>=2 and \
        isinstance(x[0], lit) and isinstance(x[-1], lit) and \
        x[0].val == "(" and x[-1].val == ")":

        if not all(isinstance(i,lit) and i.val == "," for i in x[2:-1:2]):
            return Fail
        items = x[1:-1:2]
        items = items[::-1]
        ret = lex("nil")
        for i in items:
            if isinstance(i, expr):
                ret = seq(lex("cons(")+seq([i])+lex(",")+seq([ret])+lex(")"))
            else:
                return Fail
        return ret
    else:
        return Fail

class list_pattern(pattern_wild):
    def __init__(self, name):
         self.pattern = list_pattern_func
         self.name = name


list_cast_rule = (list_pattern("x"), list_pattern("x"))
gen_list_rules = to_rules("""nil=nil
cons($x,$y)=cons($x,$y)""")
base_list_rules = [list_cast_rule]
list_rules = base_list_rules + gen_list_rules
