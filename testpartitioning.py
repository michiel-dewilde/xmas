import aggdraw, colorsys, json, random
from PIL import Image, ImageDraw
from scripts.partitioning import Partitioning, width, height

def copy_paste_rgba(src, dst, box=None):
    srcnoalpha = src.copy()
    srcnoalpha.putalpha(255)
    dst.paste(srcnoalpha, box=box, mask=src)
    
def alpha_composite_rgba(src, dst, box=None):
    dst.alpha_composite(src, dest=((0,0) if box is None else box))

#layout = json.loads('{"h":[{"v":["a","a","a"]},{"v":["a","a"]}]}')
layout = json.loads('{"ccw":{"a":1,"c":"a","d":["a","a","a","a"]}}')
weights = {'a': 1.0}
part = Partitioning(layout=layout, weights=weights)

imgsize = (width, height)

hiliteimg = Image.new("RGBA", imgsize, (255, 255, 255, 0))
slingerimg = Image.new("L", imgsize, 0)
canvas = aggdraw.Draw(slingerimg)
bulbsimg = Image.new("RGBA", imgsize, (0, 0, 0, 0))

for fe in part.tiling.fes:
    if fe.slinger is None:
        continue
    fe.slinger.draw_core(canvas)
    for light in fe.slinger.lights:
        color = tuple(round(255 * i) for i in colorsys.hsv_to_rgb(random.random(), 1.0, 1.0))
        #color = 'gold' if light.beat == 0 or light.beat == 1 else 'silver'
        light.draw_highlight(hiliteimg, color)
        light.draw_bulb(bulbsimg, color)

canvas.flush()

blendedimg = hiliteimg.copy()
blendedimg.paste("darkgreen", mask=slingerimg)
copy_paste_rgba(bulbsimg, blendedimg)

resultimg = Image.new("RGBA", imgsize, "black")
copy_paste_rgba(blendedimg, resultimg)
resultimg.show()
