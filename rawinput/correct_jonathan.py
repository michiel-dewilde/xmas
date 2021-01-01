import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', 'asax1-jonathan.mov', '-r', '30', '-vf', 
    'colorlevels=rimin=0:gimin=0:bimin=0:rimax=0.95:gimax=0.82:bimax=1,eq=gamma_r=1.5:gamma_g=1.5:gamma_b=1.5', 
    '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', os.path.join(os.pardir, 'input', 'asax1-jonathan.mp4')])