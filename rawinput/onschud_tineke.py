import subprocess, os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
for basename in ['mall-tineke1', 'mall-tineke2']:
    subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', f'{basename}.mp4', '-vf', f'vidstabdetect=stepsize=32:shakiness=10:accuracy=10:result={basename}.trf', '-f', 'null' ,'-'])
    subprocess.check_call([os.path.join(os.pardir, 'ffmpeg.exe'), '-i', f'{basename}.mp4', '-vf', f'vidstabtransform=input={basename}.trf:zoom=0:smoothing=100,unsharp=5:5:0.8:3:3:0.4', '-crf', '12' ,'-acodec', 'copy', os.path.join(os.pardir, 'input', f'{basename}.mp4')])
