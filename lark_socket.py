# experimental
import socket
from lark_str import str_val, to_lark_str
from lark_utils import Fail
from lexer import to_rules, lex
from terms import builtin_func, lit, wild, seq, expr, pattern_wild


port = 0
host = ""

class lark_socket(expr):
    normal = True
    def __init__(self):
        self.socket = socket.socket()
    def match(self, x):
        if isinstance(x, lark_socket) and self == x:
            return {}
        else:
            return Fail
    def __repr__(self):
        # super?
        return "socket()"
    def parse(self, x, exprs):
        return self.match(x)

class socket_wild(wild): # just matches ints (subs for any...)
    lazy = False
    def match(self, x):
        if isinstance(x, lark_socket) or isinstance(x, socket_wild): # should include int_wild
            ret = {}
            ret[self.name] = x
            return ret
        else:
            return Fail
    def __repr__(self):
        return "socket:"+self.name
    def parse(self, x, exprs): #NEEDED?
        attempt = self.match(x)
        if attempt == Fail:
            return Fail
        return attempt[self.name]

def socket_pattern_func(x, exprs = None):
    # this needs to bundle things methinks
    if (isinstance(x, seq) and all(isinstance(i, lit) for i in x)):
        # so... its getting passed a sequence...
        if isinstance(x,lit):
            str_val = x.val
        else:
            str_val = "".join(str(i.val) for i in x)
        if str_val == "socket()":
            return lark_socket()
        else:
            return Fail
    return Fail


    return Fail
class socket_pattern(pattern_wild):
    def __init__(self, name):
         self.pattern = socket_pattern_func
         self.name = name
    def __repr__(self):
        return "socket_pattern:" + str(self.name)
    memed = {}
    def parse(self, x, exprs):
        memed = self.memed
        if x in memed:
            return memed[x]
        memed[x] = self.pattern(x, exprs )
        return memed[x]


class open_socket_func(builtin_func):
    lazys = ["callback"]
    def __init__(self, socket, host, port, callback):
        self.socket = socket
        self.host = host
        self.port = port
        self.callback = callback

        def func_open_socket(matched_dict, exprs):
            sock = matched_dict[self.socket].socket
            host = str_val(matched_dict[self.host])
            port = int(matched_dict[self.port])
            sock.connect((host, port))
            print("connected")
            return matched_dict[self.callback].lazy_exe(exprs)
        self.func = func_open_socket

    def __repr__(self):
        return self.socket.__repr__() + ".open " + self.host.__repr__() + " " + \
            self.port.__repr__() + " " + self.callback.__repr__()

class recv_socket_func(builtin_func):

    def __init__(self, socket, num):
        self.socket = socket
        self.num = num
        def func_recv_socket(matched_dict, exprs):
            sock = matched_dict[self.socket].socket
            num = matched_dict[self.num]
            # print(matched_dict)
            msg = sock.recv(num)
            print("recieved", str(msg.decode("utf-8")).__repr__()) # converts from bytes in Python 3
            return to_lark_str(str(msg.decode("utf-8")))
        self.func = func_recv_socket

    def __repr__(self):
        return self.socket.__repr__() + ".recv " + self.num.__repr__()
from lark_utils import flatten
from lark_str import str_val
class send_socket_func(builtin_func):
    lazys = ["callback"]
    def __init__(self, socket, msg, callback):
        self.socket = socket
        self.msg = msg
        self.callback = callback
        def func_send_socket(matched_dict, exprs):
            sock = matched_dict[self.socket].socket
            msg = matched_dict[self.msg]
            print("sending", str_val(msg))
            #sendall???
            sock.sendall(str.encode(str_val(msg))) # converts to bytes in Python 3
            return matched_dict[self.callback].lazy_exe(exprs)
        self.func = func_send_socket

    def __repr__(self):
        return self.socket.__repr__() + ".send " + self.msg.__repr__() + \
        " " +  self.callback.__repr__()

lark_true = lex("True")
lark_false = lex("False")
import select
class has_data_socket_func(builtin_func):

    def __init__(self, socket):
        self.socket = socket
        def func_has_data_socket(matched_dict, exprs):
            sock = matched_dict[self.socket].socket
            rs, ws, es = select.select([sock], [sock], [sock])
            if len(rs) == 1:
                return lark_true
            else:
                return lark_false
        self.func = func_has_data_socket

    def __repr__(self):
        return self.socket.__repr__() + ".has_data"

new_socket_rule = (socket_pattern("x"), socket_pattern("x"))

open_socket_rule = (seq([socket_wild("socket"), lit("."), lit("open"),
                wild("host"), wild("port"), wild("callback")]),
                open_socket_func("socket", "host", "port", "callback"))

recv_socket_rule = (seq([socket_wild("socket"), lit("."), lit("recv"),
                wild("num")]),
                recv_socket_func("socket", "num"))

send_socket_rule = (seq([socket_wild("socket"), lit("."), lit("send"),
                wild("msg"), wild("callback")]),
                send_socket_func("socket", "msg", "callback"))

has_data_socket_rule = (seq([socket_wild("socket"), lit("."), lit("has_data")]),
                has_data_socket_func("socket"))


# NAMED VARS!!
gen_socket_rules = to_rules("""
$s.open $x $y $z = $s.open $x $y $z
$s.recv $x = $s.recv $x
$s.send $x $y = $s.send $x $y
$s.has_data = $s.has_data
""")

base_socket_rules = [new_socket_rule, open_socket_rule, recv_socket_rule,
                    send_socket_rule, has_data_socket_rule]
socket_rules = base_socket_rules + gen_socket_rules
