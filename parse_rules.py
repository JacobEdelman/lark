import parse_expr
from lark_utils import Fail, flatten2
def parse_forms(raw_rules, parser_rules = None):
    if parser_rules == None:
        parser_rules = raw_rules
    rules = []
    for i in range(len(raw_rules)):
        current = raw_rules.pop()
        trying_form, trying_out = current

        attempt_form = parse_expr.parse_expr(trying_form, [(i[0],i[0]) for i in rules+raw_rules]) #include raw forms instead?
        final_form = trying_form
        if attempt_form != Fail:
            final_form = attempt_form
        rules.append((final_form, trying_out))

    return rules

def parse_outs(raw_rules, parser_rules= None):
    if parser_rules == None:
        parser_rules = raw_rules
    parse_with =  [(i[0],i[0]) for i in parser_rules]
    rules = []
    for current in raw_rules: # this reverses order
        trying_form, trying_out = current
        attempt_out = parse_expr.parse_expr(trying_out, parse_with)
        final_out = trying_out
        if attempt_out != Fail:
            final_out = attempt_out
        rules.append((trying_form, final_out)) # this
    return order_rules(rules)

def order_rules(base_rules):
    ret = []
    base_rules.reverse() # should make ordering correct...
    while base_rules:
        rules = [i for i in base_rules] # keeps base_rules order
        for i in rules:
            current= rules.pop()
            if all((current[0].match(r[0]) == Fail or r[0].match(current[0]) != Fail) for r in rules):
                ret.append(current)
                base_rules = [i for i in base_rules if i!=current]
                break
            else:
                rules = [current] + rules

    ret.reverse()
#    raise "DONE"
    return ret


def post_parse_rules(sorted_rules):
    unambigous_rules_temp = []
    sorted_rules.reverse()
    for current in sorted_rules:
        if all((current[0].match(i[0]) != Fail or i[0].match(current[0]) == Fail) for i in sorted_rules): # no need to popping
            unambigous_rules_temp.append(current)

    unambigous_rules = []
    rules = []

    for i in range(len(sorted_rules)):
        current_rule = sorted_rules.pop()

        trying_form, trying_out = current_rule
    #    attempt_out = parse_expr.parse_expr(trying_out, unambigous_rules_temp) #include raw forms instead?
        new_form = trying_form.exe_parts(sorted_rules+[(trying_form, trying_form)])
        new_rule=(new_form, trying_out) # self exec pervention...
        # if attempt_out == Fail:
        #     new_rule=((trying_form.exe_parts(unambigous_rules_temp), trying_out)) # self exec pervention...
        # else:
        #     new_rule=((trying_form.exe_parts(unambigous_rules_temp), attempt_out))
        rules.append(new_rule)
        if current_rule in unambigous_rules_temp:
            unambigous_rules.append(new_rule)
        sorted_rules = [current_rule] + sorted_rules

    unambigous_rules = parse_forms(unambigous_rules)
    unambigous_rules.reverse()
    return parse_outs(rules, unambigous_rules), unambigous_rules
from lark_utils import flatten2
from sys import exit

def parse_rules(raw_rules):
    return post_parse_rules(parse_forms(order_rules(raw_rules)))
