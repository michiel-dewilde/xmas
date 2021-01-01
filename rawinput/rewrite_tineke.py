import subprocess, os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
for basename in ['mall-tineke1', 'mall-tineke2']:
    subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', f'{basename}.mp4', '-r', '30', '-crf', '12', '-acodec', 'copy', os.path.join(os.pardir, 'input', f'{basename}.mp4')])
