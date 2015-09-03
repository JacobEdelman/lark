from lark_utils import Fail,dict_union
class lit:
    normal = True
    lazy = True #things don't compile down to lits
    def __init__(self, val):
        self.val = val

    def match(self, x):
        # so.... nah... no execing needed?
        if isinstance(x, lit) and self.val == x.val:
            return {}
        else:
            return Fail
    def sub(self, matched_dict):
        return self

    def __repr__(self):
        return `self.val`
    def lazy_exe(self,exprs):
        return self
    def exe(self,exprs):
        return self

class expr:
    lazy = False
    normal = False

            # lazy exec sets everything on lazy mode so when
    def exe_parts(self,exprs):
        return self
    def lazy_parts_exe(self, x, exprs):
        return x

    def lazy_exe(self, exprs): # should memoize after normal
    # so... other exe.. lazy
        if self.normal:
            return self
        current = self
        for input_form, output_form in exprs:
            current = input_form.lazy_parts_exe(current, exprs)

            # should be wild?
            attempt = input_form.match(current)

            if attempt != Fail:
                attempt = output_form.sub(attempt)
                if attempt == self:
                    attempt.normal = True
                    return attempt
                else:
                    ret=attempt.lazy_exe(exprs)
                    ret.normal = True
                    return ret

        # what if I just assume its a normal form then??? that should work... yeah
        assert("I should not be here" == False) # bad style?
    def exe(self, exprs):
        return self.lazy_exe(exprs)


    def match(self, x):
        return Fail
    def sub(self, matched_dict):
        return self
times = 0
class wild(expr):
    normal = True
    lazy = True
    def __init__(self, name):
        self.name = name

    def match(self, x):
        if isinstance(x, expr):
            ret = {}
            ret[self.name] = x
            return ret
        else:
            return Fail

    def sub(self, matched_dict):
        if self.name in matched_dict:
            return matched_dict[self.name]
        return self

    def exe(self, exprs):
        return self
    def lazy_exe(self, exprs):
        return self
    def __repr__(self):
        return self.name

class seq(tuple, expr):
    def exe_parts(self, exprs):

        return seq([i.exe(exprs) for i in self]) # should this be lazy_exe??nah
    def lazy_parts_exe(self, x, exprs): # I think this works?
        if isinstance(x, seq) and len(x) == len(self): # this should report back
            return seq(input_term if my_term.lazy else input_term.lazy_exe(exprs)
                        for my_term, input_term in zip(self, x))
        else:
            return x
    def exe(self, exprs):

        #OKAY?
        ret = self.lazy_exe(exprs).exe_parts(exprs)
        ret.normal = True
        return ret

    def match(self, x):

        if isinstance(x, seq) and len(self) == len(x):

            matched_dicts = tuple(match_term.match(term) for match_term, term in zip(self, x))
            if Fail in matched_dicts:
                return Fail
            else:
                return dict_union(matched_dicts)

        else:
            return Fail

    def sub(self, matched_dict):
        if len(self) == 1 and isinstance(self[0], expr):
            return self[0].sub(matched_dict)
        return seq(i.sub(matched_dict) for i in self)

class builtin_func(wild):
    lazy = False
    def __init__(self, func):
        self.func = func

    def sub(self, matched_dict):
        return self.func(matched_dict)

class pattern_wild(wild):
    lazy = False
    def __init__(self, name, pattern):
        self.pattern = pattern
        self.name = name

    def match(self, x):
        # ummmm...


        # if isinstance(x,lit) or (isinstance(x, seq) and all(isinstance(i, lit) for i in x)):
        #     if isinstance(x,lit):
        #         str_val = x.val
        #     else:
        #         str_val = "".join(str(i.val) for i in x)
        attempt = self.pattern(x)

        if attempt != Fail: # Fail
            ret = {}
            ret[self.name] = attempt
            return ret
        else:
            return Fail
