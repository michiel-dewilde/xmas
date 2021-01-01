import os, subprocess

for i in os.listdir(os.curdir):
    if i.startswith('otbn'):
        subprocess.check_call(['ffmpeg.exe', '-y', '-i', i, '-vf', 'colorbalance=rm=-0.1:rh=-0.2:gs=0.1:gm=0.1:gh=0.0:bs=0.3:bm=0.3:bh=0.3', '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', i[1:]])