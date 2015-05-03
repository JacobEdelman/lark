import parse_expr
from lark_utils import Fail
def pre_parse_rules(raw_rules):

    rules = []
    for i in range(len(raw_rules)):
        current = raw_rules.pop()
        trying_form, trying_out = current

        attempt_form = parse_expr.parse_expr(trying_form, map(lambda i:(i[0],i[0]),rules+raw_rules)) #include raw forms instead?
        attempt_out = parse_expr.parse_expr(trying_out, map(lambda i:(i[0],i[0]),rules+raw_rules+ [current]))
        final_form = trying_form
        final_out = trying_out
        if attempt_form != Fail:
            final_form = attempt_form
        if attempt_out != Fail:
            final_out = attempt_out
        rules.append((final_form, final_out))

    return rules

def parse_with_rules(raw_rules, parser_rules):
    parse_with =  map(lambda i:(i[0],i[0]),parser_rules)
    rules = []
    for current in raw_rules: # this reverses order
        trying_form, trying_out = current
        attempt_form = parse_expr.parse_expr(trying_form,parse_with) #include raw forms instead?
        attempt_out = parse_expr.parse_expr(trying_out, parse_with)
        final_form = trying_form
        final_out = trying_out
        if attempt_form != Fail:
            final_form = attempt_form
        if attempt_out != Fail:
            final_out = attempt_out
        rules.append((final_form, final_out)) # this
    return order_rules(rules)

def order_rules(rules):
    ret = []
    while rules:
        current= rules.pop()
        if not any((current[0].match(i[0]) != Fail and i[0].match(current[0]) == Fail) for i in rules):
            ret.append(current)
        else:
            rules = [current] + rules
    ret.reverse()
#    raise "DONE"
    return ret
def parse_rules(raw_rules):
    return post_parse_rules(order_rules(pre_parse_rules(raw_rules)))

def post_parse_rules(sorted_rules):
    unambigous_rules_temp = []
    for current in sorted_rules:
        if all((current[0].match(i[0]) != Fail or i[0].match(current[0]) == Fail) for i in sorted_rules): # no need to popping
            unambigous_rules_temp.append(current)

    unambigous_rules = []
    rules = []

    for i in range(len(sorted_rules)):
        current_rule = sorted_rules.pop()
        # do not include self....
        trying_form, trying_out = current_rule
    #    attempt_out = parse_expr.parse_expr(trying_out, unambigous_rules_temp) #include raw forms instead?
        new_form = trying_form.exe_parts(sorted_rules+[(trying_form, trying_form)])
        new_rule=((new_form, trying_out)) # self exec pervention...
        # if attempt_out == Fail:
        #     new_rule=((trying_form.exe_parts(unambigous_rules_temp), trying_out)) # self exec pervention...
        # else:
        #     new_rule=((trying_form.exe_parts(unambigous_rules_temp), attempt_out))
        rules.append(new_rule)
        if current_rule in unambigous_rules_temp:
            unambigous_rules.append(new_rule)
        sorted_rules = [current_rule] + sorted_rules

    # fin_rules = []
    # for form,out in fin_rules:
    #
    #     fin_rules.append((, parse_expr.parse_expr(out, unambigous_rules)))
    return parse_with_rules(rules, unambigous_rules), unambigous_rules
