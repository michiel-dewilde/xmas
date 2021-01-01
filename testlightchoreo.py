import aggdraw, colorsys, json, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scripts import lightchoreo
from scripts.partitioning import Partitioning
from scripts.slinger import Slinger
from scripts.howbig import Howbig
from scripts.common import *
from scripts.lightchoreo import choreo, framerate, maxtime
import moviepy.editor

size = (1920, 1080)
layout = json.loads('{"h": [{"ccw":{"a":1,"c":"a","d":["a","a","a","a"]}}, {"h":[{"v":["a","a","a"]},{"v":["a","a"]}]}]}')
#layout = json.loads('{"h": [{"v":["a","a"]},{"v":["a","a"]}]}')
weights = {'a': 1.0}
part = Partitioning(size=size, layout=layout, weights=weights)

class Rotating_color_tile:
    def __init__(self, size):
        self.tile = tile
        self.basehue = random.random()
        w, h = size
        self.result = np.empty((h, w, 3), dtype=np.uint8)
    def __call__(self, t):
        hue = self.basehue + 0.1 * t
        hue = hue - math.floor(hue)
        self.result[:,:] =  tuple(round(255 * i) for i in colorsys.hsv_to_rgb(hue, 1.0, 0.1))
        return self.result

clips = []
for tile in part.tiling.tiles:
    maskvideo = moviepy.video.VideoClip.ImageClip(np.array(tile.mask)/255, is_mask=True)
    clips.append(moviepy.video.VideoClip.VideoClip(make_frame=Rotating_color_tile(tile.mask.size)).with_mask(maskvideo).with_position(tile.maskpos))

tilevideo = moviepy.editor.CompositeVideoClip(clips=clips, size=size)

class Tiles_with_lights:
    def __init__(self, tilevideo, part):
        self.tilevideo = tilevideo
        self.part = part
    def __call__(self, t):
        workimg = tilevideo.get_frame(t)
        choreoframe = round(framerate * t)
        for fe in part.tiling.fes:
            if fe.slinger is None:
                continue
            for light in fe.slinger.lights:
                rgb = lightchoreo.choreo[choreoframe, light.globalindex]
                light.hsvcolor = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
                light.draw_highlight_np(workimg, light.hsvcolor)
        workimg[:,:] = ((np.multiply(255 - self.part.overlay_img_np[:,:,3,np.newaxis], workimg[:,:], dtype='uint16')
                       + np.multiply(self.part.overlay_img_np[:,:,3,np.newaxis], self.part.overlay_img_np[:,:,0:3], dtype='uint16')) // 255).astype('uint8')
        for fe in part.tiling.fes:
            if fe.slinger is None:
                continue
            for light in fe.slinger.lights:
                light.draw_bulb_l_np(workimg, light.hsvcolor)
        return workimg

comp = moviepy.video.VideoClip.VideoClip(make_frame=Tiles_with_lights(tilevideo, part)).with_duration(maxtime).subclip(45, 60)

#comp = moviepy.editor.CompositeVideoClip(clips=clips, size=blendedimg.size).with_duration(10)
comp.write_videofile("lightchoreo.mp4", fps=framerate, preset='slow', ffmpeg_params=['-profile:v','high','-crf','17','-coder','1','-g','15','-bf','2','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1'], logger='bar')
