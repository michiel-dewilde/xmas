import moviepy.editor, os
import moviepy.video.fx
import numpy as np
from PIL import Image
import svgwrite
from scripts.sheets import minputs

os.makedirs(os.path.join('data','snap'), exist_ok=True)
os.makedirs(os.path.join('data','avg'), exist_ok=True)
os.makedirs(os.path.join('data','rect'), exist_ok=True)

for minput in minputs.values():
    if not os.path.splitext(minput.filename)[1] in ['.mov', '.m4v', '.mp4']:
        continue
    movie = os.path.join('input', minput.filename)

    filename_noext = os.path.splitext(minput.filename)[0]

    snap = os.path.join('data','snap', filename_noext + '.png')
    avg = os.path.join('data','avg', filename_noext+ '.png')

    if not os.path.exists(snap) or not os.path.exists(avg):
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

    rect = os.path.join('data','rect', filename_noext + '.svg')
    if not os.path.exists(rect):
        svgimg = Image.open(avg)
        size = svgimg.size
        dwg = svgwrite.Drawing(rect, profile='tiny', viewBox=(f'0 0 {size[0]} {size[1]}'))
        dwg.add(dwg.image(f'../avg/{filename_noext}.png', insert=(0,0), size=(size[0],size[1])))
        stroke_width = round(max(size[0], size[1]) / 192)
        dwg.add(dwg.rect(insert=(0,0), size=(size[0],size[1]), id='cbox', fill='none', stroke=svgwrite.rgb(0,0,100,'%'), stroke_width=stroke_width))
        dwg.add(dwg.rect(insert=(0,0), size=(size[0],size[1]), id='kbox', fill='none', stroke=svgwrite.rgb(0,100,0,'%'), stroke_width=stroke_width))
        dwg.add(dwg.rect(insert=(0,0), size=(size[0],size[1]), id='mbox', fill='none', stroke=svgwrite.rgb(100,100,0,'%'), stroke_width=stroke_width))
        dwg.add(dwg.rect(insert=(0,0), size=(size[0],size[1]), id='hbox', fill='none', stroke=svgwrite.rgb(100,0,0,'%'), stroke_width=stroke_width))
        dwg.save()
