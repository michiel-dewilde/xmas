import json

def calc_w(layout, weights):
    if isinstance(layout, str):
        return weights[layout]
    assert isinstance(layout, dict)
    assert len(layout) == 1
    key, value = next(iter(layout.items()))
    if key == 'bg':
        return float(value)
    if key == 'h' or key == 'v':
        return sum(calc_w(item, weights) for item in value)
    if 'key == cw' or key == 'ccw':
        return sum((calc_w(item, weights) for item in value['d']), calc_w(value['c'], weights))
    assert False

def set_seq(first, second):
    first.next = second
    second.prev = first

class Tile:
    def __init__(self):
        self.top = None # Subhe1
        self.left = None # Subhe1
        self.bot = None # Subhe1
        self.right = None # Subhe1
        self.contents = contents

class P:
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y

class Subhe1:
    def __init__(self, he, min, max):
        self.he = he
        self.min = min # P
        self.max = max # P
        self.prev = None # He1
        self.next = None # He1
        self.tile = None # Recipe (or None outside everything)

class He1:
    def __init__(self, edge, ispos, min, max):
        self.edge = edge # E1
        self.ispos = ispos # bool
        subhe = Subhe1(self, min, max)
        self.first = subhe # Sub_he1
        self.last = subhe # Sub_he1
        self.twin = None # He1

class E1:
    def __init__(self, hv, min ,max):
        self.hv = hv # 'h' or 'v'
        self.min = min # P
        self.max = max # P
        nhe = He1(self, False, min, max)
        phe = He1(self, True, min, max)
        nhe.twin = phe
        phe.twin = nhe
        self.hes = [nhe, phe]

class Tiling:
    def create_tile(self, top, left, bot, right, layout):
        set_seq(top, left)
        set_seq(left, bot)
        set_seq(bot, right)
        set_seq(right, top)
    def calc_tiling(self):
        topleft = P(0,0)
        topright = P(self.size[0],0)
        botleft = P(0,self.size[1])
        botright = P(self.size[0],self.size[1])
        self.top = E1('h', topleft, topright)
        self.left = E1('v', topleft, botleft)
        self.bot = E1('h', botleft, botright)
        self.right = E1('v', topright, botright)
        self.e1s = [self.top, self.left, self.bot, self.right]
        # outer ccb
        set_seq(self.top.hes[1], self.right.hes[1])
        set_seq(self.right.hes[1], self.bot.hes[0])
        set_seq(self.bot.hes[0], self.left.hes[0])
        set_seq(self.left.hes[0], self.top.hes[1])
        self.create_tile(self.top.hes[0], self.left.hes[1], self.bot.hes[1], self.right.hes[0], self.layout)
    def __init__(self, size, layout, weights):
        self.size = size
        self.layout = layout
        self.weights = weights
        self.recipes = []
        self.calc_tiling()

tiling = Tiling(size = (1920,1080), layout = json.loads('{"h":[{"v":["a","a","a"]},{"v":["a","a"]}]}'), weights = {'a': 1.0})
print(calc_w(tiling.layout, tiling.weights))

from pprint import pprint
pprint(vars(tiling))