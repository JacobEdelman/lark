from lark_utils import Fail
from terms import builtin_func, pattern_wild, expr, wild, seq, lit
from lexer import to_rules, lex
import string
# add in one item list
def list_pattern_func(x, exprs = None):
    if isinstance(x,lit) and x.val == "()": # shouldn't happen..
        return lex("nil")
    elif isinstance(x,seq) and len(x)==4 and \
        isinstance(x[0], lit) and isinstance(x[2], lit) and \
        isinstance(x[3], lit) and x[0].val == "(" and \
        x[2].val == "," and x[3].val == ")":
        item = x[1]
        if exprs == None:
            if isinstance(item, expr):
                return seq(lex("cons(")+seq([item])+lex(",")+seq([lex("nil")])+lex(")"))
        else:
            attempt = wild("x").parse(item, exprs)
            if attempt != Fail:
                return seq(lex("cons(")+seq([attempt])+lex(",")+seq([lex("nil")])+lex(")"))
        return Fail
    elif isinstance(x,seq) and len(x)>=5 and \
        isinstance(x[0], lit) and isinstance(x[-1], lit) and \
        x[0].val == "(" and x[-1].val == ")":
        if not all(isinstance(i,lit) and i.val == "," for i in x[2:-1:2]):
            return Fail
        items = x[1:-1:2]
        items = items[::-1]
        ret = lex("nil")
        for i in items:
            if exprs == None:
                if isinstance(i, expr):
                    ret = seq(lex("cons(")+seq([i])+lex(",")+seq([ret])+lex(")"))
                    continue
            else:
                attempt = wild("x").parse(seq([i]), exprs)
                if attempt != Fail:
                    ret = seq(lex("cons(")+seq([attempt])+lex(",")+seq([ret])+lex(")"))
                    continue
            return Fail
        return ret
    else:
        return Fail

class list_pattern(pattern_wild):
    def __init__(self, name):
         self.pattern = list_pattern_func
         self.name = name
    memed = {}
    def parse(self, x, exprs):
        memed = self.memed
        if x in memed:
            return memed[x]
        memed[x] = self.pattern(x, exprs )
        return memed[x]


list_cast_rule = (list_pattern("x"), list_pattern("x"))
gen_list_rules = to_rules("""nil=nil
cons($a,$b)=cons($a,$b)""")
base_list_rules = [list_cast_rule]
list_rules = base_list_rules + gen_list_rules
