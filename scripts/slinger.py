import aggdraw, colorsys, math, os, random
from PIL import Image, ImageDraw
import numpy as np
import scipy.stats as st
from .common import *
from .howbig import Howbig

class Slingerkern:
    def __init__(self, w, hh, wiggle, kernside, nsig, nlights, lv=0, rv=0):
        assert w > 0
        assert int(w) == w
        self.w = w
        self.hh =hh
        self.wiggle = wiggle
        self.kernside = kernside
        self.nsig = nsig
        self.nlights = nlights
        self.lv = lv
        self.rv = rv
        self.calcslinger()
        self.calclightpos()
    def calcslinger(self):
        kernel = gkern1d(2*self.kernside+1, self.nsig)
        coordinates = [(0, self.lv), (self.w, self.rv)]
        while True:
            newcoordinates = []
            unchanged = True
            last = None
            for coordinate in coordinates:
                if not last:
                    last = coordinate
                    continue
                newcoordinates.append(last)
                next = coordinate
                step = next[0] - last[0]
                if step > 1:
                    unchanged = False
                    stephw = step*self.wiggle
                    middlex = (last[0] + next[0]) // 2
                    middley = (last[1] + next[1]) / 2
                    newy = random.uniform(max(-self.hh,middley-stephw), min(self.hh,middley+stephw))
                    newcoordinates.append((middlex, newy))
                last = next
            newcoordinates.append(last)
            if unchanged:
                break
            coordinates = newcoordinates
        yonly = np.array([coordinate[1] for coordinate in coordinates])
        paddedy = np.pad(yonly, self.kernside, mode='reflect', reflect_type='odd')
        self.traject = np.convolve(paddedy, kernel, 'valid')
    def calclightpos(self):
        self.lightpos = []
        n = self.nlights
        if n == 0:
            return
        difftraject = np.diff(self.traject)
        arclens = np.sqrt(np.square(difftraject) + 1)
        cumarclen = np.cumsum(arclens)
        arclen = cumarclen[-1]
        rarclen = arclen / n
        arcposs = (0.5 + np.arange(n)) * rarclen
        xs = np.interp(arcposs, cumarclen, np.arange(len(cumarclen)))
        for x in xs:
            xi = int(x)
            xf = x - xi
            y0 = self.traject[xi]
            rc = difftraject[xi]
            y = y0 + rc * xf
            self.lightpos.append((x,y,rc))

class Light:
    def __init__(self, slinger):
        self.slinger = slinger
        self.index = None
        self.beat = None
        self.orient = None
        self.knot = None
        self.bulbrotation = None
        self.stickend = None
        self.bulbcenter = None
    def screen_cropped_point(self, point):
        size = self.slinger.howbig.size
        return (min(max(point[0], 0), size[0]), min(max(point[1], 0), size[1]))
    def prepare_highlight(self):
        howbig = self.slinger.howbig
        bigblot_size = (howbig.bigblot_side, howbig.bigblot_side)
        bigblot_center = (bigblot_size[0]/2, bigblot_size[1]/2)
        blot_scale = howbig.blot_scale
        smallblot_offgrid_center = (blot_scale*bigblot_center[0], blot_scale*bigblot_center[1])
        smallblot_pos = (math.floor(self.bulbcenter[0] - smallblot_offgrid_center[0]), math.floor(self.bulbcenter[1] - smallblot_offgrid_center[1]))
        smallblot_ongrid_center = (self.bulbcenter[0] - smallblot_pos[0], self.bulbcenter[1] - smallblot_pos[1])
        bigblot_ongrid_left_extra = round((smallblot_ongrid_center[0] - smallblot_offgrid_center[0]) / blot_scale)
        bigblot_ongrid_top_extra = round((smallblot_ongrid_center[1] - smallblot_offgrid_center[1]) / blot_scale)
        smallblot_ongrid_w = math.ceil((bigblot_size[0] + bigblot_ongrid_left_extra) * blot_scale)
        smallblot_ongrid_h = math.ceil((bigblot_size[1] + bigblot_ongrid_top_extra) * blot_scale)
        bigblot_ongrid_w = round(smallblot_ongrid_w / blot_scale)
        bigblot_ongrid_h = round(smallblot_ongrid_h / blot_scale)
        self.smallblot_pos_cropped = self.screen_cropped_point(smallblot_pos)
        smallblot_botright_cropped = self.screen_cropped_point((smallblot_pos[0] + smallblot_ongrid_w, smallblot_pos[1] + smallblot_ongrid_h))

        bigblot_ongrid = Image.new("L", (bigblot_ongrid_w, bigblot_ongrid_h), 0)
        bigblot_ongrid.paste(howbig.bigblot, (bigblot_ongrid_left_extra, bigblot_ongrid_top_extra))
        smallblot_ongrid = bigblot_ongrid.resize((smallblot_ongrid_w, smallblot_ongrid_h))
        smallblot_cropbox = (self.smallblot_pos_cropped[0]-smallblot_pos[0], self.smallblot_pos_cropped[1]-smallblot_pos[1],
                             smallblot_botright_cropped[0]-smallblot_pos[0], smallblot_botright_cropped[1]-smallblot_pos[1])
        self.smallblot_ongrid_cropped = smallblot_ongrid.crop(smallblot_cropbox)
        

    def prepare_bulb(self):
        howbig = self.slinger.howbig
        rbulb_u = howbig.bulb_unlit.rotate(self.bulbrotation, expand=True)
        rbulb_l = howbig.bulb_lightonly.rotate(self.bulbrotation, expand=True)
        rbulb_size = rbulb_u.size
        rbulb_center = (rbulb_size[0]/2, rbulb_size[1]/2)
        bulb_scale = howbig.bulb_scale
        rsbulb_offgrid_center = (bulb_scale*rbulb_center[0], bulb_scale*rbulb_center[1])
        rsbulb_pos = (math.floor(self.stickend[0] - rsbulb_offgrid_center[0]), math.floor(self.stickend[1] - rsbulb_offgrid_center[1]))
        rsbulb_ongrid_center = (self.stickend[0] - rsbulb_pos[0], self.stickend[1] - rsbulb_pos[1])
        rbulb_ongrid_left_extra = round((rsbulb_ongrid_center[0] - rsbulb_offgrid_center[0]) / bulb_scale)
        rbulb_ongrid_top_extra = round((rsbulb_ongrid_center[1] - rsbulb_offgrid_center[1]) / bulb_scale)
        rsbulb_ongrid_w = math.ceil((rbulb_size[0] + rbulb_ongrid_left_extra) * bulb_scale)
        rsbulb_ongrid_h = math.ceil((rbulb_size[1] + rbulb_ongrid_top_extra) * bulb_scale)
        rbulb_ongrid_w = round(rsbulb_ongrid_w / bulb_scale)
        rbulb_ongrid_h = round(rsbulb_ongrid_h / bulb_scale)
        self.rsbulb_pos_cropped = self.screen_cropped_point(rsbulb_pos)
        rsbulb_botright_cropped = self.screen_cropped_point((rsbulb_pos[0] + rsbulb_ongrid_w, rsbulb_pos[1] + rsbulb_ongrid_h))
        rsbulb_cropbox = (self.rsbulb_pos_cropped[0]-rsbulb_pos[0], self.rsbulb_pos_cropped[1]-rsbulb_pos[1],
                          rsbulb_botright_cropped[0]-rsbulb_pos[0], rsbulb_botright_cropped[1]-rsbulb_pos[1])

        rbulb_u_ongrid = Image.new("RGBA", (rbulb_ongrid_w, rbulb_ongrid_h), (0, 0, 0, 0))
        copy_paste_rgba(rbulb_u, rbulb_u_ongrid, (rbulb_ongrid_left_extra, rbulb_ongrid_top_extra))
        rsbulb_u_ongrid = rbulb_u_ongrid.resize((rsbulb_ongrid_w, rsbulb_ongrid_h))
        self.rsbulb_u_ongrid_cropped = rsbulb_u_ongrid.crop(rsbulb_cropbox)

        rbulb_l_ongrid = Image.new("RGBA", (rbulb_ongrid_w, rbulb_ongrid_h), (0, 0, 0, 0))
        copy_paste_rgba(rbulb_l, rbulb_l_ongrid, (rbulb_ongrid_left_extra, rbulb_ongrid_top_extra))
        rsbulb_l_ongrid = rbulb_l_ongrid.resize((rsbulb_ongrid_w, rsbulb_ongrid_h))
        self.rsbulb_l_ongrid_cropped = rsbulb_l_ongrid.crop(rsbulb_cropbox)
    def prepare_bitmaps(self):
        self.prepare_highlight()
        self.prepare_bulb()
    def draw_highlight(self, hiliteimg, color):
        coloredblotimg = Image.new("RGBA", self.smallblot_ongrid_cropped.size, color)
        coloredblotimg.putalpha(self.smallblot_ongrid_cropped)
        hiliteimg.paste(coloredblotimg, self.smallblot_pos_cropped, coloredblotimg)
    def draw_bulb_u(self, bulbsimg):
        alpha_composite_rgba(self.rsbulb_u_ongrid_cropped, bulbsimg, self.rsbulb_pos_cropped)
    def draw_bulb_l(self, bulbsimg, color):
        bulbsimg.paste(color, self.rsbulb_pos_cropped, self.rsbulb_l_ongrid_cropped)

# idealEnd should be exactly right of or exactly below idealBegin
class Slinger:
    def __init__(self, howbig, idealBegin, idealEnd, actualBegin, actualEnd):
        self.howbig = howbig
        if idealBegin[0] < idealEnd[0] and idealBegin[1] == idealEnd[1]:
            self.type = 'h'
            kern_w = actualEnd[0] - actualBegin[0]
            kern_lv = actualBegin[1] - idealBegin[1]
            kern_rv = actualEnd[1] - idealEnd[1]
        elif idealBegin[0] == idealEnd[0] and idealBegin[1] < idealEnd[1]:
            self.type = 'v'
            kern_w = actualEnd[1] - actualBegin[1]
            kern_lv = idealBegin[0] - actualBegin[0]
            kern_rv = idealEnd[0] - actualEnd[0]
        else:
            assert False, "Not h or v"
        nlights =  4 * round(kern_w / self.howbig.lightspacing / 4)
        kern = Slingerkern(w=kern_w, hh=self.howbig.hh, wiggle=0.2, kernside=15, nsig=3, nlights=nlights, lv=kern_lv, rv=kern_rv)
        if self.type == 'h':
            self.traject = [(actualBegin[0]+i, idealBegin[1]+kern.traject[i]) for i in range(kern_w+1)]
        else:
            self.traject = [(idealBegin[0]-kern.traject[i], actualBegin[1]+i) for i in range(kern_w+1)]
        self.lights = []
        for i in range(len(kern.lightpos)):
            light = Light(self)
            light.index = i
            light.beat = i % 4
            light.orient = (0 if type == 'h' else -1 if i % 2 == 0 else 1, 0 if type == 'v' else 1 if i % 2 == 0 else -1)
            lp_x,lp_y,lp_rc = kern.lightpos[i]
            light.knot = (actualBegin[0]+lp_x, idealBegin[1]+lp_y) if self.type == 'h' else (idealBegin[0]-lp_y, actualBegin[1]+lp_x)
            invnorm = 1 / math.hypot(1, lp_rc)
            muldir = light.orient[1 if type == 'h' else 0]
            dirvec = (lp_rc*invnorm*muldir, -invnorm*muldir) if self.type == 'h' else (invnorm*muldir, lp_rc*invnorm*muldir)
            degrees = math.atan2(dirvec[1], dirvec[0])*180/math.pi
            light.bulbrotation = -90-degrees
            light.stickend = (light.knot[0]+self.howbig.stick*dirvec[0], light.knot[1]+self.howbig.stick*dirvec[1])
            light.bulbcenter = (light.knot[0]+self.howbig.knottobulb*dirvec[0], light.knot[1]+self.howbig.knottobulb*dirvec[1])
            light.prepare_bitmaps()
            self.lights.append(light)
    def draw_core(self, canvas):
        path = aggdraw.Path()
        for i in range(len(self.traject)):
            (path.moveto if i == 0 else path.lineto)(self.traject[i][0], self.traject[i][1])
        canvas.path(path, self.howbig.slinger_core_pen)
        for light in self.lights:
            path = aggdraw.Path()
            path.moveto(light.knot[0], light.knot[1])
            path.lineto(light.bulbcenter[0], light.bulbcenter[1])
            canvas.path(path, self.howbig.slinger_core_pen)
