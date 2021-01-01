import os
from scripts.arrclip import make_arrclip
from scripts.lightchoreo import framerate
from scripts.tempo import m2t, t2m
from scripts.arrdata import arrdatas

os.makedirs('half', exist_ok=True)

for arrdata in arrdatas.values():
    print(f"arr {arrdata.id}")
    destfile = os.path.join('half', f'{arrdata.id}.mp4')
    if os.path.exists(destfile):
        continue
    clip = make_arrclip(arrdata.id, arrdata.box).subclip(arrdata.start,arrdata.end)
    clip.write_videofile(destfile, fps=framerate, preset='fast', ffmpeg_params=['-crf','12'], logger='bar', audio=False)
