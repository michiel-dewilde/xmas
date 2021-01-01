from scripts.arrclip import make_arrclip
from scripts.lightchoreo import framerate

clip = make_arrclip('11', 'mbox').subclip(0,200)#.subclip(30,60)
clip.write_videofile("arrclip.mp4", fps=framerate, preset='veryfast', ffmpeg_params=['-profile:v','high','-crf','17','-coder','1','-g','15','-bf','2','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1'], logger='bar')
