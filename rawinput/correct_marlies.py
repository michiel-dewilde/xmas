import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', 'fl-marlies.mov', '-vf', 
    'colorlevels=rimin=0.01:gimin=0:bimin=0.01:rimax=0.8:gimax=0.83:bimax=0.9,eq=gamma_r=1.6:gamma_g=1.6:gamma_b=1.6', 
    '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', os.path.join(os.pardir, 'input', 'fl-marlies.mp4')])