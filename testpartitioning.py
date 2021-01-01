import aggdraw, colorsys, json, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scripts.partitioning import Partitioning, width, height
from scripts.common import *

#layout = json.loads('{"h":[{"v":["a","a","a"]},{"v":["a","a"]}]}')
layout = json.loads('{"h": [{"ccw":{"a":1,"c":"a","d":["a","a","a","a"]}}, {"h":[{"v":["a","a","a"]},{"v":["a","a"]}]}]}')
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

for tile in part.tiling.tiles:
    color = tuple(round(255 * i) for i in colorsys.hsv_to_rgb(random.random(), 1.0, 1.0))
    tileimg = Image.new("RGB", tile.mask.size, color)
    resultimg.paste(tileimg, box=tile.maskpos, mask=tile.mask)
copy_paste_rgba(blendedimg, resultimg)
resultimg.show()

#assert False

import moviepy.editor

class Rotating_color_tile:
    def __init__(self, size):
        self.tile = tile
        self.basehue = random.random()
        w, h = size
        self.result = np.zeros((h, w, 3))
    def __call__(self, t):
        hue = self.basehue + 0.1 * t
        hue = hue - math.floor(hue)
        self.result[:,:] =  tuple(round(255 * i) for i in colorsys.hsv_to_rgb(hue, 1.0, 0.3))
        return self.result

clips = []
for tile in part.tiling.tiles:
    maskvideo = moviepy.video.VideoClip.ImageClip(np.array(tile.mask)/255, is_mask=True)
    clips.append(moviepy.video.VideoClip.VideoClip(make_frame=Rotating_color_tile(tile.mask.size)).with_mask(maskvideo).with_position(tile.maskpos))

tilevideo = moviepy.editor.CompositeVideoClip(clips=clips, size=blendedimg.size)

class Tiles_with_lights:
    def __init__(self, tilevideo, lightimg):
        self.tilevideo = tilevideo
        self.lightimg = lightimg
        self.lightrgb = self.lightimg[:,:,:3]
        self.lightalpha = self.lightimg[:,:,3] / 255
        self.lightalphargb = np.repeat(self.lightalpha[:,:,np.newaxis], 3, axis=2)
        self.complightalphargb = 1 - self.lightalphargb
        self.result = np.zeros(self.lightrgb.shape)
    def __call__(self, t):
        tilergb = tilevideo.get_frame(t)
        self.result[:,:] = self.complightalphargb * tilergb[:,:] + self.lightalphargb * self.lightrgb[:,:]
        return self.result

comp = moviepy.video.VideoClip.VideoClip(make_frame=Tiles_with_lights(tilevideo, np.array(blendedimg))).with_duration(10)

#comp = moviepy.editor.CompositeVideoClip(clips=clips, size=blendedimg.size).with_duration(10)
comp.write_videofile("hues.mp4", fps=30, preset='slow', ffmpeg_params=['-profile:v','high','-crf','22','-coder','1','-g','15','-bf','2','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1'], logger='bar')