# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


import lexer
import parse_rules
import lark_utils
import terms
import parse_expr
import sys
# <codecell>


Fail = lark_utils.Fail

import lark_int, lark_list


def exe_text(x): #BAD
    rules = []
    to_eval = []
    for i in x.split("\n"):
        if "=" in i:
            rules.append(i)
        else:
            to_eval.append(i)
    exprs = lark_int.int_rules + lark_list.list_rules
    exprs += map(lexer.to_rule,rules)
    exprs, parser_exprs = parse_rules.parse_rules(exprs)
    exprs.reverse()

    print "Rules Compiled"
    compiled_parts = []
    for i in to_eval:
        i = i.strip()
        if i!="":
            compiled_parts.append(parse_expr.parse_expr(lexer.lex(i), parser_exprs))
    print "Expressions Compiled"
    for i in compiled_parts:
        print lark_utils.flatten(i.exe(exprs))





def main():
    if len(sys.argv) == 1:
        print "At least one argument needed"
    else:
        text = ""
        for f in sys.argv[1:]:
            opened_file = open(f)
            text += opened_file.read()+"\n"
            opened_file.close()
        exe_text(text)

if __name__ == "__main__":
    main()
# for i in exprs:
#     print i

# # prog = "f(15)"
# # #
# #
# print lark_utils.flatten(parse_expr.parse_expr(lexer.lex("if True f(10) else f(30)"),exprs).exe(exprs)).replace("'","")
# <codecell>

# import cProfile
# cProfile.run('x=17;print str(parse_expr.parse_expr(lexer.lex("f(19)"),exprs).exe(exprs))')
