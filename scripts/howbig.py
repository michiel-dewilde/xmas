import aggdraw, colorsys, math, os, random
from PIL import Image, ImageDraw
import numpy as np
import scipy.stats as st
from .common import *

slinger_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slinger_data')
gbulb_unlit_rgb = Image.open(os.path.join(slinger_data, 'bulb-unlit-rgb.png'))
gbulb_unlit_a = Image.open(os.path.join(slinger_data, 'bulb-unlit-a.png'))
gbulb_unlit = Image.new("RGBA", gbulb_unlit_rgb.size, (0, 0, 0, 0))
gbulb_unlit.paste(gbulb_unlit_rgb)
gbulb_unlit.putalpha(gbulb_unlit_a)
gbulb_lightonly = Image.open(os.path.join(slinger_data, 'bulb-lightonly.png'))

#size = (1920//2, 1080//2)
size = (1920, 1080)
#size = (2*1920, 2*1080)

timeoffset = 2
totalduration = 190

class Howbig:
    def __init__(self, size, weight):
        self.size = size
        scale = math.sqrt(size[0]/1920 * size[1]/1080 * 5/weight)
        self.hh = round(20 * scale)
        self.stick = 10 * scale
        self.bulbsize = 3 * self.stick
        self.knottobulb = self.stick + 2/3 * self.bulbsize
        self.lightspacing = 50 * scale

        bulbsrc_initheight = 4 * (2*self.bulbsize)
        bulbsrc_new_size = (round(bulbsrc_initheight*gbulb_unlit.size[0]/gbulb_unlit.size[1]), round(bulbsrc_initheight))
        self.bulb_unlit = gbulb_unlit.resize(bulbsrc_new_size)
        self.bulb_lightonly = gbulb_lightonly.resize(bulbsrc_new_size)

        self.bulb_scale = self.bulbsize / (self.bulb_unlit.size[1] / 2)
        self.slinger_core_pen = aggdraw.Pen(255, 4.0 * scale, linecap=2)

        self.blotsize = 100 * scale
        self.bigblot_side = round(4 * self.blotsize)
        self.blot_scale = self.blotsize / self.bigblot_side
        blotkernel = gkern2d(self.bigblot_side, 3)
        blotkernel = np.round(blotkernel*(255/np.max(blotkernel)))
        blotdata = np.zeros((self.bigblot_side, self.bigblot_side), dtype=np.uint8)
        blotdata[:,:] = blotkernel
        self.bigblot = Image.fromarray(blotdata, 'L')