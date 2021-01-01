import os
from os.path import splitext
from scripts.arrparse import get_arr_layout

import aggdraw, colorsys, json, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scripts.partitioning import Partitioning
from scripts.common import *

from scripts.sheets import minputs

weights = {}
size = (1920, 1080)

for key, minput in minputs.items():
    weights[key] = minput.weight

for filename in os.listdir(os.path.join('data', 'arr')):
    key, ext = os.path.splitext(filename)
    if ext != '.svg':
        continue
    print(f'{key}:')
    layout = get_arr_layout(key)

    part = Partitioning(size=size, layout=layout, weights=weights)

    workimg = Image.new("RGBA", size, "black")
    black = True
    for tile in part.tiling.tiles:
        color = tuple(round(255 * i) for i in colorsys.hsv_to_rgb(random.random(), 1.0, 0.5))
        #color = "black" if black else "white"
        black = not black
        tileimg = Image.new("RGB", tile.mask.size, color)
        workimg.paste(tileimg, box=tile.maskpos, mask=tile.mask)

    on = True

    for fe in part.tiling.fes:
        if fe.slinger is None:
            continue
        for light in fe.slinger.lights:
            light.hsvcolor = (random.random(), random.random(), 1) if on else (0,0,0)
            light.draw_highlight(workimg, light.hsvcolor)
            #on = not on

    alpha_composite_rgba(part.overlay_img, workimg)

    for fe in part.tiling.fes:
        if fe.slinger is None:
            continue
        for light in fe.slinger.lights:
            light.draw_bulb_l(workimg, light.hsvcolor)

    workimg.show()