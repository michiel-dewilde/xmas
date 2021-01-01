import colorsys
import json
import math
import os
import random
from os.path import splitext

import aggdraw
import moviepy.editor
import numpy as np
from PIL import Image, ImageDraw, ImageOps

from . import lightchoreo
from .arrparse import get_arr_layout
from .common import *
from .cropsize import Cropdata
from .howbig import Howbig
from .lightchoreo import choreo, framerate, maxtime, maxframe
from .partitioning import Partitioning
from .sheets import minputs
from .slinger import Slinger
from .rects import keyRects, Rect
from .tempo import m2t, t2m

class Clip_with_lights:
    def __init__(self, srcvideo, part):
        self.srcvideo = srcvideo
        self.part = part
    def __call__(self, t):
        workimg = self.srcvideo.get_frame(t)
        choreoframe = min(round(framerate * t), maxframe-1)
        for fe in self.part.tiling.fes:
            if fe.slinger is None:
                continue
            for light in fe.slinger.lights:
                rgb = lightchoreo.choreo[choreoframe, light.globalindex]
                light.hsvcolor = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
                light.draw_highlight_np(workimg, light.hsvcolor)
        workimg[:,:] = ((np.multiply(255 - self.part.overlay_img_np[:,:,3,np.newaxis], workimg[:,:], dtype='uint16')
                       + np.multiply(self.part.overlay_img_np[:,:,3,np.newaxis], self.part.overlay_img_np[:,:,0:3], dtype='uint16')) // 255).astype('uint8')
        for fe in self.part.tiling.fes:
            if fe.slinger is None:
                continue
            for light in fe.slinger.lights:
                light.draw_bulb_l_np(workimg, light.hsvcolor)
        return workimg

def get_tileclip(tile, id, whichbox):
        minput = minputs[id]
        rects = keyRects[id]
        cropdata = Cropdata((rects.bbox.w, rects.bbox.h), getattr(rects, whichbox), rects.hbox, tile.mask.size, Rect(0, 0, tile.mask.size[0], tile.mask.size[1]))

        ffmpegsize = cropdata.size
        if minput.rotation == 'ccw' or minput.rotation == 'cw':
            ffmpegsize = ffmpegsize[::-1]

        clip = moviepy.editor.VideoFileClip(os.path.join('input', minput.filename), target_resolution=ffmpegsize).without_audio()
        clip.rotation = 0

        if minput.rotation == 'ccw':
            clip = clip.fx(moviepy.video.fx.rotate, 90)
        elif minput.rotation == 'cw':
            clip = clip.fx(moviepy.video.fx.rotate, 270)

        if minput.mirrored:
            clip = clip.fx(moviepy.video.fx.mirror_x)

        clip = clip.fx(moviepy.video.fx.crop, x1=cropdata.crop.x, y1=cropdata.crop.y, width=cropdata.crop.w, height=cropdata.crop.h)
        
        maskvideo = moviepy.video.VideoClip.ImageClip(np.array(tile.mask)/255, is_mask=True)
        return clip.with_mask(maskvideo).with_position(tile.maskpos)

def make_arrclip(akey, whichbox):
    weights = {}
    size = (1920, 1080)
    for mkey, minput in minputs.items():
        weights[mkey] = minput.weight
    layout = get_arr_layout(akey)
    part = Partitioning(size=size, layout=layout, weights=weights)

    clips = []
    for tile in part.tiling.tiles:
        id = tile.id
        clip = get_tileclip(tile, id, whichbox)
        minput = minputs[id]
        delay = minput.delay
        if delay < 0:
            clip = clip.subclip(-delay)
        else:
            clip = clip.with_start(delay)
        clips.append(clip)
        if akey == '11':
            if 'perc1' in tile.id:
                id = 'timp-koend'
                clip = get_tileclip(tile, id, whichbox)
                minput = minputs[id]
                delay = minput.delay
                timpstart = m2t(16)
                timpend = m2t(20)
                timpcf = m2t(16.5)-m2t(16)
                clip = clip.subclip(timpstart-delay, timpend-delay).crossfadein(timpcf).crossfadeout(timpcf).with_start(timpstart)
                clips.append(clip)
            if 'perc2' in tile.id:
                id = 'perc2-vj1'
                clip = get_tileclip(tile, id, whichbox)
                minput = minputs[id]
                delay = minput.delay
                vjstart = m2t(18)
                vjend = m2t(25)
                clip = clip.subclip(vjstart-delay, vjend-delay).crossfadein(m2t(18.5)-m2t(18)).with_start(vjstart)
                clips.append(clip)

    comp = moviepy.editor.CompositeVideoClip(clips=clips, size=size)
    return moviepy.video.VideoClip.VideoClip(make_frame=Clip_with_lights(comp, part))
