import subprocess, os
for basename in ['cl1-heleenba', 'cl2-heleenba']:
    subprocess.check_call([os.path.join(os.pardir, os.pardir, 'ffmpeg.exe'), '-y', '-i', f'{basename}.mp4', '-vf', f'vidstabdetect=stepsize=32:shakiness=10:accuracy=10:result={basename}.trf', '-f', 'null' ,'-'])
    subprocess.check_call([os.path.join(os.pardir, os.pardir, 'ffmpeg.exe'), '-y', '-i', f'{basename}.mp4', '-vf', f'vidstabtransform=input={basename}.trf:zoom=0:smoothing=30,unsharp=5:5:0.8:3:3:0.4', '-crf', '12' ,'-acodec', 'copy', os.path.join(os.pardir, f'{basename}.mp4')])
