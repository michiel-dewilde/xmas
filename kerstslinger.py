import aggdraw, colorsys, math, os, random
from PIL import Image, ImageDraw
import numpy as np
import scipy.stats as st

def gkern1d(kernlen, nsig):
    x = np.linspace(-nsig, nsig, kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    return kern1d/kern1d.sum()

def gkern2d(kernlen, nsig):
    x = np.linspace(-nsig, nsig, kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kern2d = np.outer(kern1d, kern1d)
    return kern2d/kern2d.sum()

class Slingerkern:
    def __init__(self, w, hh, wiggle, kernside, nsig, nlights, lv=None, rv=None):
        assert w > 0
        assert int(w) == w
        self.w = w
        self.hh =hh
        self.wiggle = wiggle
        self.kernside = kernside
        self.nsig = nsig
        self.nlights = nlights
        self.lv = random.uniform(-self.hh,self.hh) if lv is None else lv
        self.rv = random.uniform(-self.hh,self.hh) if rv is None else rv
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
        assert abs(self.traject[0]-self.lv) < 0.5
        assert abs(self.traject[-1]-self.rv) < 0.5
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

hh = 20
stick = 10.
bulbsize = 3 * stick
knottobulb = stick + 2/3 * bulbsize
lightspacing = 50

bulb_unlit_rgb = Image.open(os.path.join('slinger', 'bulb-unlit-rgb.png'))
bulb_unlit_a = Image.open(os.path.join('slinger', 'bulb-unlit-a.png'))
bulb_unlit = Image.new("RGBA", bulb_unlit_rgb.size, (0, 0, 0, 0))
bulb_unlit.paste(bulb_unlit_rgb)
bulb_unlit.putalpha(bulb_unlit_a)
bulbratio = bulbsize / (bulb_unlit.size[1] / 2)
bulb_lightonly = Image.open(os.path.join('slinger', 'bulb-lightonly.png'))

class Light:
    def __init__(self):
        self.index = None
        self.beat = None
        self.orient = None
        self.knot = None
        self.bulbrotation = None
        self.stickend = None
        self.bulbcenter = None

# idealEnd should be exactly right of or exactly below idealBegin
class Slinger:
    def __init__(self, idealBegin, idealEnd, actualBegin, actualEnd):
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
        nlights =  4 * round(kern_w / lightspacing / 4)
        kern = Slingerkern(w=kern_w, hh=hh, wiggle=0.2, kernside=15, nsig=3, nlights=nlights, lv=kern_lv, rv=kern_rv)
        if self.type == 'h':
            self.traject = [(actualBegin[0]+i, idealBegin[1]+kern.traject[i]) for i in range(kern_w+1)]
        else:
            self.traject = [(idealBegin[0]-kern.traject[i], actualBegin[1]+i) for i in range(kern_w+1)]
        self.lights = []
        for i in range(len(kern.lightpos)):
            light = Light()
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
            light.stickend = (light.knot[0]+stick*dirvec[0], light.knot[1]+stick*dirvec[1])
            light.bulbcenter = (light.knot[0]+knottobulb*dirvec[0], light.knot[1]+knottobulb*dirvec[1])
            self.lights.append(light)

def copy_paste_rgba(src, dst, box=None):
    srcnoalpha = src.copy()
    srcnoalpha.putalpha(255)
    dst.paste(srcnoalpha, box=box, mask=src)
    
def alpha_composite_rgba(src, dst, box=None):
    dst.alpha_composite(src, dest=((0,0) if box is None else box))

blotsize = 150
blotkernel = gkern2d(blotsize, 3)
blotkernel = np.round(blotkernel*(192/np.max(blotkernel)))
blotdata = np.zeros((blotsize, blotsize), dtype=np.uint8)
blotdata[:,:] = blotkernel
blotimage = Image.fromarray(blotdata, 'L')

slingers = []

iTopleft = (100, 100)
aTopleft = (iTopleft[0]+random.randrange(-hh,hh+1), iTopleft[1]+random.randrange(-hh,hh+1))
iTopright = (600, 100)
aTopright = (iTopright[0]+random.randrange(-hh,hh+1), iTopright[1]+random.randrange(-hh,hh+1))
iBotleft = (100, 600)
aBotleft = (iBotleft[0]+random.randrange(-hh,hh+1), iBotleft[1]+random.randrange(-hh,hh+1))
iBotright = (600, 600)
aBotright = (iBotright[0]+random.randrange(-hh,hh+1), iBotright[1]+random.randrange(-hh,hh+1))

slingers.append(Slinger(iTopleft, iTopright, aTopleft, aTopright))
slingers.append(Slinger(iBotleft, iBotright, aBotleft, aBotright))
slingers.append(Slinger(iTopleft, iBotleft, aTopleft, aBotleft))
slingers.append(Slinger(iTopright, iBotright, aTopright, aBotright))

imgsize = (700, 700)

hiliteimg = Image.new("RGBA", imgsize, (255, 255, 255, 0))
slingerimg = Image.new("L", imgsize, 0)
canvas = aggdraw.Draw(slingerimg)
bulbsimg = Image.new("RGBA", imgsize, (0, 0, 0, 0))

pen = aggdraw.Pen(255, 4.0)

for slinger in slingers:
    path = aggdraw.Path()
    for i in range(len(slinger.traject)):
        (path.moveto if i == 0 else path.lineto)(slinger.traject[i][0], slinger.traject[i][1])
    canvas.path(path, pen)
    for light in slinger.lights:
        color = tuple(round(255 * i) for i in colorsys.hsv_to_rgb(random.random(), 1.0, 1.0))
        color = 'gold' if light.beat == 0 or light.beat == 1 else 'silver'
    
        # blots
        coloredblotimg = Image.new("RGBA", blotimage.size, color)
        coloredblotimg.putalpha(blotimage)
        hiliteimg.paste(coloredblotimg, (round(light.bulbcenter[0]-blotsize/2),round(light.bulbcenter[1]-blotsize/2)), coloredblotimg)
        
        # sticks
        path = aggdraw.Path()
        path.moveto(light.knot[0], light.knot[1])
        path.lineto(light.bulbcenter[0], light.bulbcenter[1])
        canvas.path(path, pen)
        
        # bulbs
        bulb = bulb_unlit.copy()
        bulb.paste(color, mask=bulb_lightonly)
        rbulb = bulb.rotate(light.bulbrotation, expand=True)
        rsbulb = rbulb.resize((round(rbulb.size[0]*bulbratio), round(rbulb.size[1]*bulbratio)))
        copy_paste_rgba(rsbulb, bulbsimg, (round(light.stickend[0]-rsbulb.size[0]/2), round(light.stickend[1]-rsbulb.size[1]/2)))

canvas.flush()

blendedimg = hiliteimg.copy()
blendedimg.paste("darkgreen", mask=slingerimg)
copy_paste_rgba(bulbsimg, blendedimg)

resultimg = Image.new("RGBA", imgsize, "black")
copy_paste_rgba(blendedimg, resultimg)
resultimg.show()

resultimg = Image.new("RGBA", imgsize, "white")
copy_paste_rgba(blendedimg, resultimg)
resultimg.show()

resultimg = Image.new("RGBA", imgsize, "grey")
copy_paste_rgba(blendedimg, resultimg)
resultimg.show()
