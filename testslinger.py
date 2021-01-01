import aggdraw, colorsys, math, os, random
from PIL import Image, ImageDraw
import numpy as np
import scipy.stats as st

from scripts.slinger import Slinger
from scripts.howbig import Howbig
from scripts.common import *

imgsize = (700, 700)

howbig = Howbig(size=imgsize, weight=1)
hh = howbig.hh

slingers = []

iTopleft = (100, 100)
aTopleft = (iTopleft[0]+random.randrange(-hh,hh+1), iTopleft[1]+random.randrange(-hh,hh+1))
iTopright = (600, 100)
aTopright = (iTopright[0]+random.randrange(-hh,hh+1), iTopright[1]+random.randrange(-hh,hh+1))
iBotleft = (100, 600)
aBotleft = (iBotleft[0]+random.randrange(-hh,hh+1), iBotleft[1]+random.randrange(-hh,hh+1))
iBotright = (600, 600)
aBotright = (iBotright[0]+random.randrange(-hh,hh+1), iBotright[1]+random.randrange(-hh,hh+1))


slingers.append(Slinger(howbig, iTopleft, iTopright, aTopleft, aTopright))
slingers.append(Slinger(howbig, iBotleft, iBotright, aBotleft, aBotright))
slingers.append(Slinger(howbig, iTopleft, iBotleft, aTopleft, aBotleft))
slingers.append(Slinger(howbig, iTopright, iBotright, aTopright, aBotright))


hiliteimg = Image.new("RGBA", imgsize, (255, 255, 255, 0))
slingerimg = Image.new("L", imgsize, 0)
canvas = aggdraw.Draw(slingerimg)
bulbsimg = Image.new("RGBA", imgsize, (0, 0, 0, 0))

for slinger in slingers:
    slinger.draw_core(canvas)
    for light in slinger.lights:
        color = tuple(round(255 * i) for i in colorsys.hsv_to_rgb(random.random(), 1.0, 1.0))
        #color = 'gold' if light.beat == 0 or light.beat == 1 else 'silver'
        light.draw_highlight(hiliteimg, color)
        light.draw_bulb_u(bulbsimg)
        light.draw_bulb_l(bulbsimg, color)

canvas.flush()

blendedimg = hiliteimg.copy()
blendedimg.paste("darkgreen", mask=slingerimg)
copy_paste_rgba(bulbsimg, blendedimg)

resultimg = Image.new("RGBA", imgsize, "black")
copy_paste_rgba(blendedimg, resultimg)
resultimg.show()
