from lark_utils import Fail, dict_union, flatten2, flatten
memed_seq = {}
wild_memed = {}

def reset_memed():
    global wild_memed
    global memed_seq
    memed_seq = {}
    wild_memed = {}


class lit:
    normal = True
    lazy = True

    def __init__(self, val):
        self.val = val

    def match(self, x):
        if isinstance(x, lit) and self.val == x.val:
            return {}
        else:
            return Fail

    def sub(self, matched_dict):
        return self

    def __repr__(self):
        return self.val.__repr__()

    def lazy_exe(self, exprs):
        return self

    def exe(self, exprs):
        return self

    def parse(self, x, exprs):
        if isinstance(x, seq):
            if len(x) != 1:
                return Fail
            attempt = self.parse(x[0], exprs)
            if attempt == Fail:
                return Fail
            elif isinstance(attempt, seq):
                return attempt
            else:
                return seq([attempt])
        elif self.match(x) == Fail:
            return Fail
        return x


tabs = 0

class expr:
    lazy = False
    normal = False

    def exe_parts(self, exprs):
        return self

    def lazy_parts_exe(self, x, exprs):
        return x

    def lazy_exe(self, exprs):
        global tabs
        if self.normal:
            return self
        current = self
        for input_form, output_form in exprs:
            tabs += 1
            current = input_form.lazy_parts_exe(current, exprs)
            attempt = input_form.match(current)
            tabs -= 1
            if attempt != Fail:

                attempt = output_form.sub(attempt)
                if attempt == self:
                    attempt.normal = True
                    return attempt
                else:
                    ret = attempt.lazy_exe(exprs)
                    ret.normal = True
                    return ret

        assert 'I should not be here' == False

    def exe(self, exprs):
        return self.lazy_exe(exprs)

    def match(self, x):
        return Fail

    def sub(self, matched_dict):
        return self

    def parse(self, x, exprs):
        return self.match(x)


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
        return '$' + self.name

    def parse(self, x, exprs):
        if isinstance(x, seq) and len(x) == 1 and isinstance(x[0], expr):
            return x
        memed = wild_memed
        if x in memed:
            return memed[x]
        memed[x] = Fail
        for expr_in, expr_out in exprs:
            attempt = expr_in.parse(x, exprs)
            if attempt != Fail:
                memed[x] = seq([attempt])
                break

        return memed[x]

class seq(tuple, expr):

    def exe_parts(self, exprs):
        return seq([ i.exe(exprs) for i in self ])

    def lazy_parts_exe(self, x, exprs):
        if isinstance(x, seq) and len(x) == len(self):
            return seq(((input_term if my_term.lazy else input_term.lazy_exe(exprs)) for my_term, input_term in zip(self, x)))
        else:
            return x


    def exe(self, exprs):
        ret = self.lazy_exe(exprs).exe_parts(exprs)
        ret.normal = True
        return ret

    def match(self, x):
        if isinstance(x, seq) and len(self) == len(x):
            ret = {}
            for match_term, term in zip(self, x):
                attempt = match_term.match(term)
                if attempt == Fail:
                    return Fail
                ret.update(attempt)

            return ret
        return Fail

    def sub(self, matched_dict):
        if len(self) == 1 and isinstance(self[0], expr):
            return self[0].sub(matched_dict)
        return seq((i.sub(matched_dict) for i in self))

    def lits(self):
        if not hasattr(self, 'memed_lits'):
            self.memed_lits = {i.val for i in self if isinstance(i, lit)}
        return self.memed_lits

    def get_midpoint(self):
        if not hasattr(self, 'memed_midpoint'):
            if self.lits():
                ret = 0
                for t in self:
                    if isinstance(t, lit):
                        break
                    ret += 1

            else:
                ret = len(self) / 2
            self.memed_midpoint = ret
            return ret
        return self.memed_midpoint

    def parse(self, x, exprs, top = 0):

        if (self, x) in memed_seq:
            return memed_seq[self, x]
        memed_seq[self, x] = Fail
        if len(self) == 1:
            ret = self[0].parse(x, exprs)
            memed_seq[self, x] = ret
            return ret
        if not isinstance(x, seq):
            pass
        elif len(self) > len(x):
            pass
        else:
            if self.lits() - x.lits():
                return Fail
            if isinstance(self[0], lit):
                if x[0].parse(self[0], exprs) == Fail:
                    return Fail
                if isinstance(self[-1], lit) and x[-1].parse(self[-1], exprs) == Fail:
                    return Fail
                midpoint = 1
                i = 1
                left_half = seq(self[:midpoint])
                left_x = seq(x[:i])
                left_attempt = left_half.parse(left_x, exprs)
                if left_attempt != Fail:
                    right_half = seq(self[midpoint:])
                    right_x = seq(x[i:])
                    right_attempt = right_half.parse(right_x, exprs)

                    if right_attempt != Fail:
                        ret = seq(left_attempt + right_attempt)
                        memed_seq[self, x] = ret
                        return ret
            elif isinstance(self[-1], lit):

                if x[-1].parse(self[-1], exprs) == Fail:
                    return Fail
                midpoint = len(self) - 1
                i = len(x) - 1
                right_half = seq(self[midpoint:])
                right_x = seq(x[i:])
                right_attempt = right_half.parse(right_x, exprs)
                if right_attempt != Fail:
                    left_half = seq(self[:midpoint])
                    left_x = seq(x[:i])
                    left_attempt = left_half.parse(left_x, exprs)
                    if left_attempt != Fail:
                        ret = seq(left_attempt + right_attempt)
                        memed_seq[self, x] = ret
                        return ret
            else:
                midpoint = self.get_midpoint()
                startpoint = midpoint

                endpoint = len(x) - len(self) // 2 + 1
                left_half = seq(self[:midpoint])
                right_half = seq(self[midpoint:])
                first_lit = self[midpoint]
                for i in range(startpoint, endpoint):
                    if i < len(x) and self.lits() and first_lit.match(x[i]) == Fail:
                        continue
                    right_x = seq(x[i:])
                    right_attempt = right_half.parse(right_x, exprs)
                    if right_attempt != Fail:
                        left_x = seq(x[:i])
                        left_attempt = left_half.parse(left_x, exprs)
                        if left_attempt != Fail:
                            ret = seq(left_attempt + right_attempt)
                            memed_seq[self, x] = ret
                            return ret
        return Fail


class builtin_func(wild):
    lazys = []
    def __init__(self, func):
        self.func = func
        self.matched_dict = {}

    def lazy_exe(self, exprs):
        for k in self.matched_dict:
            if k not in self.lazys:
                self.matched_dict[k] = self.matched_dict[k].exe(exprs)

        return self.func(self.matched_dict)

    def sub(self, matched_dict):
        for k in matched_dict:
            matched_dict[k] = matched_dict[k].sub(matched_dict)

        self.matched_dict = matched_dict
        return self

    def parse(self, x, exprs):
        attempt = self.match(x)
        if attempt == Fail:
            return Fail
        else:
            return seq([x])


class pattern_wild(wild):

    def __init__(self, name, pattern):
        self.pattern = pattern
        self.name = name

    def match(self, x):
        attempt = self.pattern(x)
        if attempt != Fail:
            ret = {}
            ret[self.name] = attempt
            return ret
        else:
            return Fail
