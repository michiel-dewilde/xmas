import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', 'tpt2-els.mov', '-vf', 
    'colorlevels=rimin=0.04:gimin=0.04:bimin=0.04:rimax=0.55:gimax=0.64:bimax=0.71,eq=gamma_r=1.77:gamma_g=1.72:gamma_b=1.77', 
    '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', os.path.join(os.pardir, 'input', 'tpt2-els.mp4')])