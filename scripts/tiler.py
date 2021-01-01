import math
import numpy as np

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
        self.fhes = []
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
        self.edge = edge
        self.ispos = ispos # bool
        self.first_ishe = Ishe(self, pmin, pmax)
        self.twin = None

class Ie: # initial edge
    def __init__(self, hv, pmin, pmax, is_outer=False):
        self.hv = hv # 'h' or 'v'
        self.pmin = pmin
        self.pmax = pmax
        nhe = Ihe(self, False, pmin, pmax)
        phe = Ihe(self, True, pmin, pmax)
        nhe.twin = phe
        phe.twin = nhe
        self.hes = [nhe, phe]
        self.is_outer = is_outer

class Fv: # final vertex
    def __init__(self, p):
        self.p = p
        self.incident = []

class Fhe: # final halfedge
    def __init__(self, edge, ispos):
        self.edge = edge
        self.ispos = ispos # bool
        self.twin = None
        self.ishe = None
        self.prev = None
        self.next = None
        self.target = None

class Fe: # final edge
    def __init__(self, ie, pmin, pmax):
        self.ie = ie
        self.pmin = pmin
        self.pmax = pmax
        nhe = Fhe(self, False)
        phe = Fhe(self, True)
        nhe.twin = phe
        phe.twin = nhe
        self.hes = [nhe, phe]

def calc_w(layout,weights):
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

class Tiling:
    def round(self, val):
        return np.round(val)

    def calc_w(self,layout):
        return calc_w(layout, self.weights)

    def process_layout(self, layout, tishe, lishe, bishe, rishe):
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
            weights = [self.calc_w(item) for item in value]
            cweights = np.cumsum(weights)
            xs = self.round(left + cweights[:-1]*((right - left) / cweights[-1]))
            ptops = [(int(x), top) for x in xs]
            ntishes = tishe.split(ptops)
            pbots = [(int(x), bot) for x in xs]
            nbishes = bishe.split(pbots)
            ies = [Ie('v', ptop, pbot) for ptop, pbot in zip(ptops, pbots)]
            self.ies += ies
            nlishes = [lishe] + [ie.hes[1].first_ishe for ie in ies]
            nrishes = [ie.hes[0].first_ishe for ie in ies] + [rishe]
            for nlayout, ntishe, nlishe, nbishe, nrishe in zip(value, ntishes, nlishes, nbishes, nrishes):
                self.process_layout(nlayout,  ntishe, nlishe, nbishe, nrishe)
            return
        if key == 'v':
            weights = [self.calc_w(item) for item in value]
            cweights = np.cumsum(weights)
            ys = self.round(top + cweights[:-1]*((bot - top) / cweights[-1]))
            plefts = [(left, int(y)) for y in ys]
            nlishes = lishe.split(plefts)
            prights = [(right, int(y)) for y in ys]
            nrishes = rishe.split(prights)
            ies = [Ie('h', pleft, pright) for pleft, pright in zip(plefts, prights)]
            self.ies += ies
            ntishes = [tishe] + [ie.hes[0].first_ishe for ie in ies]
            nbishes = [ie.hes[1].first_ishe for ie in ies] + [bishe]
            for nlayout, ntishe, nlishe, nbishe, nrishe in zip(value, ntishes, nlishes, nbishes, nrishes):
                self.process_layout(nlayout,  ntishe, nlishe, nbishe, nrishe)
            return
        if 'key == cw' or key == 'ccw':
            W = right - left
            H = bot - top
            g = self.calc_w(value['c'])
            G = sum((self.calc_w(item) for item in value['d']), g)
            a = value['a']
            w = math.sqrt(a*W*H*g/G)
            h = w/a
            x0 = left
            x1 = int(self.round(left + (W-w)/2))
            x2 = int(self.round(left + (W+w)/2))
            x3 = right
            y0 = top
            y1 = int(self.round(top + (H-h)/2))
            y2 = int(self.round(top + (H+h)/2))
            y3 = bot
            if ('key' == 'cw'):
                toishes = tishe.split([(x2, y0)])
                roishes = rishe.split([(x3, y2)])
                boishes = bishe.split([(x1, y3)])
                loishes = lishe.split([(x0, y1)])

                tiie = Ie('h', (x0, y1), (x2, y1))
                biishe = tiie.hes[1].first_ishe
                tcishes = tiie.hes[0].first_ishe.split([(x1, y1)])                

                riie = Ie('v', (x2, y0), (x2, y2))
                liishe = riie.hes[1].first_ishe
                rcishes = riie.hes[0].first_ishe.split([(x2, y1)])                

                biie = Ie('h', (x1, y2), (x3, y2))
                tiishe = biie.hes[0].first_ishe
                bcishes = biie.hes[1].first_ishe.split([(x2, y2)])                
                
                liie = Ie('v', (x1, y1), (x1, y3))
                riishe = liie.hes[0].first_ishe
                lcishes = liie.hes[1].first_ishe.split([(x2, y1)])                

                self.ies += [tiie, riie, biie, liie]
                self.process_layout(value['c'], tcishes[1], lcishes[0], bcishes[0], rcishes[1])
                self.process_layout(value['d'][0], toishes[0], loishes[0], biishe, rcishes[0])
                self.process_layout(value['d'][1], toishes[1], liishe, bcishes[1], roishes[0])
                self.process_layout(value['d'][2], tiishe, lcishes[1], boishes[1], roishes[1])
                self.process_layout(value['d'][3], tcishes[0], loishes[1], boishes[0], riishe)
            else:
                toishes = tishe.split([(x1, y0)])
                loishes = lishe.split([(x0, y2)])
                boishes = bishe.split([(x2, y3)])
                roishes = rishe.split([(x3, y1)])

                liie = Ie('v', (x1, y0), (x1, y2))
                riishe = liie.hes[0].first_ishe
                lcishes = liie.hes[1].first_ishe.split([(x1, y1)])

                biie = Ie('h', (x0, y2), (x2, y2))
                tiishe = biie.hes[0].first_ishe
                bcishes = biie.hes[1].first_ishe.split([(x1, y2)])                
                
                riie = Ie('v', (x2, y1), (x2, y3))
                liishe = riie.hes[1].first_ishe
                rcishes = riie.hes[0].first_ishe.split([(x2, y2)])                

                tiie = Ie('h', (x1, y1), (x3, y1))
                biishe = tiie.hes[1].first_ishe
                tcishes = tiie.hes[0].first_ishe.split([(x2, y1)])                

                self.ies += [liie, biie, riie, tiie]
                self.process_layout(value['c'], tcishes[0], lcishes[1], bcishes[1], rcishes[0])
                self.process_layout(value['d'][0], toishes[0], loishes[0], bcishes[0], riishe)
                self.process_layout(value['d'][1], tiishe, loishes[1], boishes[0], rcishes[1])
                self.process_layout(value['d'][2], tcishes[1], liishe, boishes[1], roishes[1])
                self.process_layout(value['d'][3], toishes[1], lcishes[0], biishe, roishes[0])
            return
        assert False

    def create_ies_tiles(self, layout):
        self.ies = []
        self.tiles = []
        topleft = (0, 0)
        topright = (self.size[0], 0)
        botleft = (0, self.size[1])
        botright = (self.size[0], self.size[1])
        self.tie = Ie('h', topleft, topright, is_outer=True)
        self.lie = Ie('v', topleft, botleft, is_outer=True)
        self.bie = Ie('h', botleft, botright, is_outer=True)
        self.rie = Ie('v', topright, botright, is_outer=True)
        self.ies += [self.tie, self.lie, self.bie, self.rie]
        self.process_layout(layout, self.tie.hes[0].first_ishe, self.lie.hes[1].first_ishe, self.bie.hes[1].first_ishe, self.rie.hes[0].first_ishe)

    def merge_ie(self, ie):
        nishe = ie.hes[0].first_ishe
        pishe = ie.hes[1].first_ishe
        pmin = ie.pmin
        while nishe is not None:
            assert pishe is not None
            pmax = min(nishe.pmax, pishe.pmax)
            fe = Fe(ie, pmin, pmax)
            self.fes.append(fe)
            nishe.fhes.append(fe.hes[0])
            fe.hes[0].ishe = nishe
            pishe.fhes.append(fe.hes[1])
            fe.hes[1].ishe = pishe
            if nishe.pmax == pmax:
                nishe = nishe.next_ishe
            if pishe.pmax == pmax:
                pishe = pishe.next_ishe
            pmin = pmax
        assert pishe is None

    def create_fes(self):
        self.fes = []
        for ie in self.ies:
            self.merge_ie(ie)

    def set_he_seq(self):
        fhes = []
        fhes.extend(self.tie.hes[1].first_ishe.fhes)
        fhes.extend(self.rie.hes[1].first_ishe.fhes)
        fhes.extend(reversed(self.bie.hes[0].first_ishe.fhes))
        fhes.extend(reversed(self.lie.hes[0].first_ishe.fhes))
        fhes.append(fhes[0])
        for first, second in zip(fhes[:-1], fhes[1:]):
            first.next = second
            second.prev = first
        for tile in self.tiles:
            fhes = []
            fhes.extend(reversed(tile.tishe.fhes))
            fhes.extend(tile.lishe.fhes)
            fhes.extend(tile.bishe.fhes)
            fhes.extend(reversed(tile.rishe.fhes))
            fhes.append(fhes[0])
            for first, second in zip(fhes[:-1], fhes[1:]):
                first.next = second
                second.prev = first

    def create_fvs(self):
        self.fvs = []
        for fe in self.fes:
            for ispos in (False, True):
                fhe = fe.hes[ispos]
                if fhe.target is not None:
                    continue
                p = (fe.pmin, fe.pmax)[ispos]
                fv = Fv(p)
                self.fvs.append(fv)
                circ = fhe
                while True:
                    circ.target = fv
                    fv.incident.append(circ)
                    circ = circ.next.twin
                    if circ == fhe:
                        break
                
    def __init__(self, size, layout, weights):
        self.size = size
        self.weights = weights
        self.create_ies_tiles(layout)
        self.create_fes()
        self.set_he_seq()
        self.create_fvs()
