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
    in_string = rets[0] == '"'
    escaped = False
    for i in x[1:]:
        index +=1
        if escaped:
            rets[-1]+=i
            escaped = False
        elif in_string:
            rets[-1]+=i
            in_string = (i != '"')
            if not in_string:
                rets.append("")
            escaped = (i == "\\")
        elif i in string.whitespace:
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
            elif i == '"' and rets[-1] == "":
                rets[-1]+=i
                in_string = True
            elif i == '"':
                rets.append(i)
                in_string = True
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
    #extra?
    expr,out = x[:x.index("=")], x[x.index("=")+1:]
    return (lex(expr),lex(out))
def break_into_parts(x):

    ret = [""]
    level = 0
    second_part = False
    multiline = False
    in_string = False
    escaped = False
    for i in x:
        to_become_second_part = False
        if escaped:
            ret[-1]+=i
            continue
        elif in_string:
            ret[-1]+=i
            in_string = (i != '"')
            escaped = (i == "\\")
            continue


        ret[-1]+=i
        if i == '"':
            in_string = True
        elif i == "{":
            level+=1
            if second_part:
                multiline = True
        elif i == "}":
            level -=1
        elif i == "=" and (not second_part) and level == 0:
            to_become_second_part = True
        if level == 0 and second_part and i == "\n":
            ret.append("")
            second_part = False
            multiline = False
        second_part |= to_become_second_part
    return ret

def to_rules(x):
    ret=[to_rule(i.strip()) for i in break_into_parts(x) if i.strip()!=""]
    return ret
