import terms
from lark_utils import Fail
from terms import wild



def parse_expr(x,exprs):
    terms.reset_memed()
    if isinstance(x,terms.wild): #SHOULD BE FINE
        return x


    if len(x) == 1:
        #ehhh?
        if isinstance(x[0],terms.expr):
            return x[0]

    attempt = wild("x").parse(x, exprs)

    if attempt != Fail and len(attempt) == 1: #WAT?
        return attempt[0]
    return attempt
