import csv, moviepy.editor, os, subprocess
import numpy as np

times = []
beats = []
with open('tempo/tempo.csv', newline='', encoding='utf-8') as f:
    for line in csv.reader(f):
        times.append(int(line[2])/48000-0.1)
        beats.append(float(int(line[0])*4+int(line[1])-1))

clip = moviepy.editor.VideoFileClip('tempo/origyt.webm')
width = clip.size[0]
height = clip.size[1]
fps = 30
#clip = clip.subclip(clip.duration - 5, clip.duration)
duration = clip.duration

txtsize = 2*int(height/5)

class Textpos:
    def __init__(self, i):
        self.i = i
    def __call__(self, t):
        if t < times[0] or t >= times[-1]:
            return (width, height)
        beat = np.interp(t, times, beats)
        intbeat = int(beat)
        fracbeat = beat - intbeat
        modbeat = intbeat % 4
        if modbeat != self.i:
            return (width, height)
        frac = fracbeat if intbeat % 2 == 0 else 1 - fracbeat
        return ((width-txtsize)/2,frac * (height-txtsize))

thomas = moviepy.editor.VideoFileClip('tempo/thomas.mp4')
thomas = thomas.crop(x1=0,y1=0,width=512,height=288).resize((width, height)).subclip(0,thomas.duration-0.1).fadein(1).fadeout(1)
#thomas = thomas.subclip(thomas.duration-2, thomas.duration)
tdur = thomas.duration

clips = [thomas,clip.with_start(tdur)]
for i in range(0,4):
    clips.append(moviepy.video.VideoClip.TextClip(text=str(i+1), size=(txtsize, txtsize), font='arial', color=['red','orange','green','blue'][i]).with_duration(duration).with_position(Textpos(i)).with_start(tdur))

clips.append(moviepy.video.VideoClip.TextClip(text="Dikke merci en tot gauw!", size=(0.8*width, height), font='arial', color='red').with_duration(2).with_position(('center','center')).with_start(tdur + duration - 4))

comp = moviepy.editor.CompositeVideoClip(clips=clips, size=(width, height)).with_duration(tdur+duration)
#comp.write_videofile("tempo/tempo.mp4", fps=fps, audio_codec='aac', audio_bitrate='384k', audio_fps=48000, logger='bar')
comp.write_videofile("tempo/tempo.mp4", fps=fps, audio_codec='aac', audio_bitrate='384k', audio_fps=48000, preset='slow', ffmpeg_params=['-profile:v','high','-crf','22','-coder','1','-g',str(fps//2),'-bf','2','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1'], logger='bar')
