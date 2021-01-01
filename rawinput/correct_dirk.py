import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', 'asax2-dirk.mov', '-vf', 
    'colorlevels=rimin=0.04:gimin=0.04:bimin=0.02:rimax=1:gimax=0.95:bimax=0.93,eq=gamma_r=1.3:gamma_g=1.3:gamma_b=1.3', 
    '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', os.path.join(os.pardir, 'input', 'asax2-dirk.mp4')])