import moviepy.editor, os
import moviepy.video.fx
import numpy as np
from PIL import Image
from scripts.sheets import minputs

os.makedirs(os.path.join('data','snap'), exist_ok=True)
os.makedirs(os.path.join('data','avg'), exist_ok=True)

for minput in minputs.values():
    if not os.path.splitext(minput.filename)[1] in ['.mov', '.m4v', '.mp4']:
        continue
    movie = os.path.join('input', minput.filename)

    snap = os.path.join('data','snap', os.path.splitext(minput.filename)[0] + '.png')
    avg = os.path.join('data','avg', os.path.splitext(minput.filename)[0] + '.png')

    if os.path.exists(snap) and os.path.exists(avg):
        continue

    clip = moviepy.editor.VideoFileClip(movie)
    if clip.rotation in (90, 270):
        clip = clip.resize(clip.size[::-1])
        clip.rotation = 0
    clip = moviepy.editor.VideoFileClip(movie, target_resolution=clip.size)
    clip.rotation = 0

    if minput.rotation == 'ccw':
        clip = clip.fx(moviepy.video.fx.rotate, 90)
    elif minput.rotation == 'cw':
        clip = clip.fx(moviepy.video.fx.rotate, 270)

    if minput.mirrored:
        clip = clip.fx(moviepy.video.fx.mirror_x)

    if not os.path.exists(snap):
        im = Image.fromarray(clip.get_frame(clip.duration/2))
        im.save(snap)

    if not os.path.exists(avg):
        previous_frame = None
        for frame in clip.iter_frames():
            if previous_frame is None:
                runsum = np.zeros(frame.shape)
            else:
                runsum += np.square(frame - previous_frame)
            previous_frame = frame
        rms = np.sqrt(np.sum(runsum, 2))
        rms = np.uint8(rms * (255 / np.amax(rms)))
        img = Image.fromarray(rms , 'L')
        img.save(avg)