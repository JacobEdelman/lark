def dict_union(x): # I want to change this for equality checking
    ret = {}
    for given_dict in x:
        for key in given_dict:
            ret[key] = given_dict[key]
    return ret

class prim_object:
    def __equ__(self,x):
        if id(equ) == id(self):
            return True
        return False
#lets make all the Fails the same

def flatten(x):
    if type(x)==str:
        return x
    if hasattr(x,"val"):
        return str(x.val)
    try:
        return "".join(map(flatten,x))
    except:
        return str(x)
Fail = prim_object()
