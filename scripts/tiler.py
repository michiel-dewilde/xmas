import json, math
import numpy as np

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
    def __init__(self, id, tishe, lishe, bishe, rishe):
        self.id = id
        self.tishe = tishe
        tishe.tile = self
        self.lishe = lishe
        lishe.tile = self
        self.bishe = bishe
        bishe.tile = self
        self.rishe = rishe
        rishe.tile = self

class Ishe: # initial subhalfedge
    def __init__(self, he, pmin, pmax):
        self.he = he
        self.pmin = pmin
        self.pmax = pmax
        self.next_ishe = None
        self.tile = None
    def split(self, points):
        ishes = []
        orig_he = self.he
        orig_pmax = self.pmax
        orig_next_ishe = self.next_ishe
        ishe_it = self
        ishes.append(ishe_it)
        for point in points:
            ishe_it.pmax = point
            ishe_it.next_ishe = Ishe(orig_he, point, None)
            ishe_it = ishe_it.next_ishe
            ishes.append(ishe_it)
        ishe_it.pmax = orig_pmax
        ishe_it.next_ishe = orig_next_ishe
        return ishes

class Ihe: # initial halfedge
    def __init__(self, edge, ispos, pmin, pmax):
        self.edge = edge # E1
        self.ispos = ispos # bool
        self.first_ishe = Ishe(self, pmin, pmax)
        self.twin = None # He1

class Ie: # initial edge
    def __init__(self, hv, pmin ,pmax):
        self.hv = hv # 'h' or 'v'
        self.pmin = pmin
        self.pmax = pmax
        nhe = Ihe(self, False, pmin, pmax)
        phe = Ihe(self, True, pmin, pmax)
        nhe.twin = phe
        phe.twin = nhe
        self.hes = [nhe, phe]

class Tiling:
    def round(self, val):
        return np.round(val)
    def create_tile(self, layout, tishe, lishe, bishe, rishe):
        if isinstance(layout, str):
            tile = Tile(layout, tishe, lishe, bishe, rishe)
            self.tiles.append(tile)
            return
        assert isinstance(layout, dict)
        assert len(layout) == 1
        key, value = next(iter(layout.items()))
        if key == 'bg':
            tile = Tile(None, tishe, lishe, bishe, rishe)
            self.tiles.append(tile)
            return
        left, top = tishe.pmin
        right, bot = bishe.pmax
        if key == 'h':
            weights = [calc_w(item, self.weights) for item in value]
            cweights = np.cumsum(weights)
            xs = self.round(left + cweights[:-1]*((right - left) / cweights[-1]))
            ptops = [(x, top) for x in xs]
            ntishes = tishe.split(ptops)
            pbots = [(x, bot) for x in xs]
            nbishes = bishe.split(pbots)
            ies = [Ie('v', ptop, pbot) for ptop, pbot in zip(ptops, pbots)]
            self.ies += ies
            nlishes = [lishe] + [ie.hes[1].first_ishe for ie in ies]
            nrishes = [ie.hes[0].first_ishe for ie in ies] + [rishe]
            for nlayout, ntishe, nlishe, nbishe, nrishe in zip(value, ntishes, nlishes, nbishes, nrishes):
                self.create_tile(nlayout,  ntishe, nlishe, nbishe, nrishe)
            return
        if key == 'v':
            weights = [calc_w(item, self.weights) for item in value]
            cweights = np.cumsum(weights)
            ys = self.round(top + cweights[:-1]*((bot - top) / cweights[-1]))
            plefts = [(left, y) for y in ys]
            nlishes = lishe.split(plefts)
            prights = [(right, y) for y in ys]
            nrishes = rishe.split(prights)
            ies = [Ie('h', pleft, pright) for pleft, pright in zip(plefts, prights)]
            self.ies += ies
            ntishes = [tishe] + [ie.hes[0].first_ishe for ie in ies]
            nbishes = [ie.hes[1].first_ishe for ie in ies] + [bishe]
            for nlayout, ntishe, nlishe, nbishe, nrishe in zip(value, ntishes, nlishes, nbishes, nrishes):
                self.create_tile(nlayout,  ntishe, nlishe, nbishe, nrishe)
            return
        if 'key == cw' or key == 'ccw':
            W = right - left
            H = bot - top
            g = calc_w(value['c'], self.weights)
            G = sum((calc_w(item, self.weights) for item in value['d']), g)
            a = value['a']
            w = math.sqrt(a*W*H*g/G)
            h = w/a
            x0 = left
            x1 = self.round(left + (W-w)/2)
            x2 = self.round(left + (W+w)/2)
            x3 = right
            y0 = top
            y1 = self.round(top + (H-h)/2)
            y2 = self.round(top + (H+h)/2)
            y3 = bot
            #maaktegels(tegels, value['c'], vopts, {'x':x1, 'y':y1, 'w':x2-x1, 'h':y2-y1})
            #if ('key' == 'cw'):
            #    maaktegels(tegels, value['d'][0], vopts, {'x':x0, 'y':y0, 'w':x2-x0, 'h':y1-y0})
            #    maaktegels(tegels, value['d'][1], vopts, {'x':x2, 'y':y0, 'w':x3-x2, 'h':y2-y0})
            #    maaktegels(tegels, value['d'][2], vopts, {'x':x1, 'y':y2, 'w':x3-x1, 'h':y3-y2})
            #    maaktegels(tegels, value['d'][3], vopts, {'x':x0, 'y':y1, 'w':x1-x0, 'h':y3-y1})
            #else:
            #    maaktegels(tegels, value['d'][0], vopts, {'x':x0, 'y':y0, 'w':x1-x0, 'h':y2-y0})
            #    maaktegels(tegels, value['d'][1], vopts, {'x':x0, 'y':y2, 'w':x2-x0, 'h':y3-y2})
            #    maaktegels(tegels, value['d'][2], vopts, {'x':x2, 'y':y1, 'w':x3-x2, 'h':y3-y1})
            #    maaktegels(tegels, value['d'][3], vopts, {'x':x1, 'y':y0, 'w':x3-x1, 'h':y1-y0})
            return
        assert False
    def calc_tiling(self):
        topleft = (0, 0)
        topright = (self.size[0], 0)
        botleft = (0, self.size[1])
        botright = (self.size[0], self.size[1])
        self.ite = Ie('h', topleft, topright)
        self.ile = Ie('v', topleft, botleft)
        self.ibe = Ie('h', botleft, botright)
        self.ire = Ie('v', topright, botright)
        self.ies += [self.ite, self.ile, self.ibe, self.ire]
        self.create_tile(self.layout, self.ite.hes[0].first_ishe, self.ile.hes[1].first_ishe, self.ibe.hes[1].first_ishe, self.ire.hes[0].first_ishe)
    def __init__(self, size, layout, weights):
        self.size = size
        self.layout = layout
        self.weights = weights
        self.ies = []
        self.tiles = []
        self.calc_tiling()

tiling = Tiling(size = (1920,1080), layout = json.loads('{"h":[{"v":["a","a","a"]},{"v":["a","a"]}]}'), weights = {'a': 1.0})

#from pprint import pprint
for tile in tiling.tiles:
    print(tile.id, tile.tishe.pmin, tile.bishe.pmax)