import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
for i in os.listdir(os.curdir):
    if i.startswith('tbn'):
        subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', i, '-vf', 'colorlevels=rimin=0:gimin=0:bimin=0:rimax=0.96:gimax=1:bimax=0.71,eq=gamma_r=1.13:gamma_g=1.28:gamma_b=1.48', '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', os.path.join(os.pardir, 'input', i)])