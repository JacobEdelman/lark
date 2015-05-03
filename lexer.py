import terms
import string
def list_to_terms(x):
    return terms.seq(terms.wild(i[1:]) if i[0]=="$" else terms.lit(i) for i in x)

def str_to_parts(x): # not good, : troubles
    x=x.strip()
    rets = [x[0]]
    wild = rets[0] == "$"
    any_part = False
    index = 0
    for i in x[1:]:
        index +=1
        if i in string.whitespace:
            if rets[-1]!="":
                rets.append("")
                wild = x[index+1] == "$"
        elif wild:
            if i == "$" and rets[-1] == "":
                rets[-1]+=i
            elif i in string.ascii_letters or (rets[-1]!="$" and i in string.digits+"_"):
                rets[-1]+=i
            else:
                rets.append(i)
                wild = False
        else:
            if i == "$":
                rets.append(i)
                wild = True
            elif rets[-1] == "":
                rets[-1]+=i
            elif i in string.ascii_letters+string.digits+"_" and rets[-1][0] in string.ascii_letters:
                rets[-1]+=i
            elif i in string.digits and rets[-1][0] in string.digits:
                rets[-1]+=i
            else:
                rets.append(i)
    if rets[0] == "":
        rets = rets[1:]
    if rets[-1] == "":
        rets = rets[:-1]
    return rets

def lex(x):
    return list_to_terms(str_to_parts(x))

def to_rule(x):
    expr,out = x.split("=")
    return (lex(expr),lex(out))

def to_rules(x):
    return map(lambda i:to_rule(i.strip()),filter(lambda i: i.strip()!="",x.split("\n")))
