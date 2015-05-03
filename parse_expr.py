import terms
from lark_utils import Fail
import random
def parse_expr(x,exprs):
    #(problem with int_wild?)
    #Good way to do it (with memoizing (exprs to tuple)):
    # split in halves,
    # for each rule, split the rule in half and try it on each part?

    if isinstance(x,terms.wild): #SHOULD BE FINE
        return x


    if len(x) == 1:
        #ehhh?
        if isinstance(x[0],terms.expr):
            return x[0]


    done = [x]
    strings = [((i,),x) for i in range(len(exprs))]
    while strings:
        place, current_str = strings.pop()
        current_expr = exprs[place[-1]][0] # the match part of it
        for l in range(1,len(current_str)+1):
            for start in range(len(current_str)-l+1):
                end = start + l # correct end index
                test_seq = terms.seq(current_str[start:end])
                attempt = current_expr.match(test_seq)
                if attempt != Fail:
                  #  attempt = parse_expr_with_list(attempt,exprs)
                    if l == len(current_str):
                        return test_seq

                    to_add = current_str[:start]+(test_seq,) + current_str[end:]

                    if to_add not in done:
                        done.append(to_add)
                        # really it should then postpone further exec uni
                        for i in range(len(exprs)):
                            strings.append((place+(i,),to_add))
    return Fail
