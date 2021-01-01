import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
for basename in ['bsn-koend']:
    subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', f'{basename}.mp4', '-vf', 'eq=gamma=1.5', '-pix_fmt' ,'yuv420p', '-an', '-crf', '18', os.path.join(os.pardir, 'input', f'{basename}.mp4')])
