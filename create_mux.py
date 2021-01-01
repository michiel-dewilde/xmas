import os, subprocess
from scripts.howbig import timeoffset, totalduration

subprocess.check_call(['ffmpeg', '-y', '-i', 'vmix.mp4', '-i', os.path.join('audio', f'xmas-master-{timeoffset}-{totalduration}.wav'),'-c:v','copy','-c:a','aac','-b:a','384k','-movflags','+faststart','-fflags','+bitexact','-map_metadata','-1','-metadata','title=All I Want For Christmas Is You','-metadata','creation_time=2020-12-19T20:00:00+0100','-metadata','date=2020-12-19','-metadata',"artist=Muziekensemble d'eaux sérieuses",'-metadata',
    'composer=Mariah Carey and Walter Afanasieff arr. Michael Brown','DS All I Want For Christmas Is You.mp4'])