import moviepy.editor, moviepy.video.fx, os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

clips = []
clip = moviepy.editor.VideoFileClip('perc2-vj1.mp4').without_audio()
flipclip = clip.fx(moviepy.video.fx.mirror_y)
clips.append(flipclip.with_position((0,0)))
clips.append(clip.with_position((0,1080)))
clips.append(flipclip.with_position((0,2*1080)))
comp = moviepy.editor.CompositeVideoClip(clips=clips, size=(1920,3*1080))

comp.write_videofile(os.path.join(os.pardir, 'input', 'perc2-vj1.mp4'), fps=30, preset='slow', ffmpeg_params=['-profile:v','high','-crf','12','-coder','1','-g','15','-bf','2','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1'], logger='bar')