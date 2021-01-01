import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', 'cl3-carolien.mov', '-vf', 
    'colorlevels=rimin=0.06:gimin=0:bimin=0:rimax=0.98:gimax=0.58:bimax=0.89,eq=gamma_r=1.04:gamma_g=1.3:gamma_b=1.3', 
    '-pix_fmt' ,'yuv420p', '-acodec', 'copy', '-crf', '18', os.path.join(os.pardir, 'input', 'cl3-carolien.mp4')])