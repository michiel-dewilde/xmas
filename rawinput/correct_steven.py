import os, subprocess
os.chdir(os.path.dirname(os.path.realpath(__file__)))
for basename in ['tsax-steven']:
    subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', f'{basename}.mov', '-vf', 'eq=gamma=1.2', '-pix_fmt' ,'yuv420p', '-an', '-crf', '18', os.path.join(os.pardir, 'input', f'{basename}.mp4')])
for basename in ['tbn-steven']:
    subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', f'{basename}.mov', '-vf', 'eq=gamma=1.3', '-pix_fmt' ,'yuv420p', '-an', '-crf', '18', os.path.join(os.pardir, 'input', f'{basename}.mp4')])