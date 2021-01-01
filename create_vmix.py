import os, subprocess
import moviepy.editor, moviepy.video.VideoClip, moviepy.video.fx
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from scripts.howbig import size
from scripts.tempo import m2t, t2m
from scripts.sheets import minputs
from scripts.arrdata import arrdatas
from scripts.lightchoreo import framerate
from scripts.howbig import timeoffset, totalduration
from scripts.fastcomposite import FastCompositeVideoClip

def frameround(t):
    return round(t*framerate)/framerate

def get_arrclip(akey, start, end = None):
    arrdata = arrdatas[akey]
    clip = moviepy.editor.VideoFileClip(os.path.join('half', f'{akey}.mp4'))
    clip = clip.subclip(start - (timeoffset + arrdata.start))
    if end:
        clip = clip.with_duration(end - start)
    return clip.with_start(start)

clips = []

logoimg = Image.open(os.path.join('media', 'DS_AIWFCIY_opening.png'))
if (list(size) != list(logoimg.size)):
    logoimg = logoimg.resize(size)
logovideo = moviepy.video.VideoClip.ImageClip(np.array(logoimg))

clips.append(logovideo.with_duration(timeoffset + 3).fadein(1))

tdelay = minputs['mall-tineke2'].delay
clip = moviepy.editor.VideoFileClip(os.path.join('input', 'mall-tineke2.mp4'), target_resolution=size)
clips.append(clip.with_duration(m2t(6)-tdelay).with_start(timeoffset + tdelay).crossfadein(2))
clips.append(get_arrclip('2', timeoffset + m2t(4) + 1).crossfadein(1))
clips.append(get_arrclip('3', timeoffset + m2t(9)))
clips.append(get_arrclip('11', timeoffset + m2t(12.75)))
clips.append(get_arrclip('a', timeoffset + m2t(79), timeoffset + m2t(84)))
clips.append(get_arrclip('b', timeoffset + m2t(83), timeoffset + m2t(88)))
clips.append(get_arrclip('c', timeoffset + m2t(87), timeoffset + m2t(92)))
clips.append(get_arrclip('d', timeoffset + m2t(91), timeoffset + m2t(95)))

#vmix = moviepy.editor.CompositeVideoClip(clips=clips, size=size).with_duration(totalduration).fadeout(1)
vmix = FastCompositeVideoClip(clips=clips, size=size).with_duration(totalduration).fadeout(1)
vmix.write_videofile('vmix.mp4', fps=framerate, preset='slow', ffmpeg_params=['-profile:v','high','-crf','22','-coder','1','-g',f'{framerate//2}','-bf','2'], logger='bar', audio=False)
#vmix.write_videofile('vmix.mp4', fps=framerate, preset='fast', ffmpeg_params=['-crf','12'], logger='bar', audio=False)
