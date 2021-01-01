import os
from scripts.arrclip import make_arrclip
from scripts.lightchoreo import framerate
from scripts.tempo import m2t, t2m
from scripts.arrdata import arrdatas

for arrdata in arrdatas.values():
    destfile = os.path.join('half', f'{arrdata.id}.mp4')
    if os.path.exists(destfile):
        continue
    clip = make_arrclip(arrdata.id, arrdata.box).subclip(arrdata.start,arrdata.end)
    clip.write_videofile(destfile, fps=framerate, preset='veryfast', ffmpeg_params=['-profile:v','high','-crf','17','-coder','1','-g','15','-bf','2','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1'], logger='bar')
