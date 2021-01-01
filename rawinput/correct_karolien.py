import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', 'fl-karolien.mov', '-vf', 
    'colorlevels=rimin=0.1:gimin=0.08:bimin=0.09:rimax=1:gimax=1:bimax=1,eq=gamma_r=1.6:gamma_g=1.6:gamma_b=1.6', 
    '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', os.path.join(os.pardir, 'input', 'fl-karolien.mp4')])