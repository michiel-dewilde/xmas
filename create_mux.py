import os, subprocess
from scripts.howbig import timeoffset, totalduration

if not os.path.exists('DS All I Want for Christmas Is You AVC.mp4'):
    subprocess.check_call(['ffmpeg', '-y', '-i', 'vmix.mp4', '-i', os.path.join('audio', f'xmas-master-{timeoffset}-{totalduration}.wav'),'-c:v','copy','-c:a','aac','-b:a','384k','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1','-metadata','title=All I Want for Christmas Is You','-metadata','creation_time=2020-12-18T21:30:00+0100','-metadata','date=2020-12-18','-metadata',"artist=Muziekensemble d'eaux sérieuses",'-metadata',
        'composer=Mariah Carey and Walter Afanasieff arr. Michael Brown','DS All I Want for Christmas Is You AVC.mp4'])
if not os.path.exists('DS All I Want for Christmas Is You HEVC.mp4'):
    subprocess.check_call(['ffmpeg', '-y', '-i', 'vmix265.mp4', '-i', os.path.join('audio', f'xmas-master-{timeoffset}-{totalduration}.wav'),'-c:v','copy','-c:a','aac','-b:a','384k','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1','-metadata','title=All I Want for Christmas Is You','-metadata','creation_time=2020-12-18T21:30:00+0100','-metadata','date=2020-12-18','-metadata',"artist=Muziekensemble d'eaux sérieuses",'-metadata',
        'composer=Mariah Carey and Walter Afanasieff arr. Michael Brown','DS All I Want for Christmas Is You HEVC.mp4'])