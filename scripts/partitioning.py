import aggdraw, math, random
from PIL import Image, ImageDraw
from .tiler import Tiling
from .slinger import Slinger
from .howbig import Howbig
from .common import *

width = 1920
height = 1080
rel_delta = 1/3

class Partitioning:
    def __init__(self, layout, weights):
        self.tiling = Tiling(size=(width, height), layout=layout, weights=weights)
        self.howbig = Howbig(self.tiling.total_weight)
        hh = self.howbig.hh
        # initial vertex range on boundary
        for fv in self.tiling.fvs:
            if fv.p[0] == 0 or fv.p[0] == width:
                fv.axmin = fv.p[0]
                fv.axmax = fv.p[0]
            else:
                fv.axmin = max(0, fv.p[0] - hh)
                fv.axmax = min(width, fv.p[0] + hh)
            if fv.p[1] == 0 or fv.p[1] == height:
                fv.aymin = fv.p[1]
                fv.aymax = fv.p[1]
            else:
                fv.aymin = max(0, fv.p[1] - hh)
                fv.aymax = min(height, fv.p[1] + hh)
        # limit vertex range based on edges
        for fe in self.tiling.fes:
            nhe, phe = fe.hes
            vmin = nhe.target
            vmax = phe.target
            if fe.ie.hv == 'h':
                d = rel_delta * (vmax.p[0] - vmin.p[0])
                v = round(vmin.p[0] + d)
                if vmin.axmax > v:
                    vmin.axmax = v
                v = round(vmax.p[0] - d)
                if vmax.axmin < v:
                    vmax.axmin = v
            else:
                d = rel_delta * (vmax.p[1] - vmin.p[1])
                v = round(vmin.p[1] + d)
                if vmin.aymax > v:
                    vmin.aymax = v
                v = round(vmax.p[1] - d)
                if vmax.aymin < v:
                    vmax.aymin = v
        # set actual vertex coordinate
        for fv in self.tiling.fvs:
            fv.ap = (random.randrange(fv.axmin,fv.axmax+1), random.randrange(fv.aymin,fv.aymax+1))
        # calculate slingers
        for fe in self.tiling.fes:
            fe.slinger = None
            if fe.ie.is_outer:
                continue
            nhe, phe = fe.hes
            vmin = nhe.target
            vmax = phe.target
            fe.slinger = Slinger(self.howbig, vmin.p, vmax.p, vmin.ap, vmax.ap)
        # calculate tile crops
        brush = aggdraw.Brush(255)
        for tile in self.tiling.tiles:
            circ_points = []
            for fhe in tile.fhes:
                if fhe.edge.slinger:
                    traject = fhe.edge.slinger.traject
                    circ_points.extend(traject if fhe.ispos else reversed(traject))
                else:
                    circ_points += [fhe.source.ap, fhe.target.ap]
            left = math.floor(min(p[0] for p in circ_points))
            right = math.ceil(max(p[0] for p in circ_points))
            top = math.floor(min(p[1] for p in circ_points))
            bot = math.ceil(max(p[1] for p in circ_points))
            tile.maskpos = (left, top)
            tile.mask = Image.new("L", (right - left, bot - top), 0)
            canvas = aggdraw.Draw(tile.mask)
            path = aggdraw.Path()
            path.moveto(circ_points[0][0], circ_points[0][1])
            for p in circ_points[1:]:
                path.lineto(p[0] - left, p[1] - top)
            canvas.path(path, None, brush)
            canvas.flush()