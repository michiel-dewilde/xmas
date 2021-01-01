import subprocess, os, sys
os.environ['PATH'] = os.pathsep.join([os.path.join(os.environ['PROGRAMFILES'], 'Git', 'cmd'), r'{0}\system32;{0};{0}\System32\Wbem'.format(os.environ['SYSTEMROOT'])])
if not os.path.exists('.venv'):
    subprocess.call([sys.executable, '-m', 'venv', '.venv'])
vpy = os.path.join('.venv', 'Scripts', 'python.exe')
subprocess.call([vpy, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
vpip = os.path.join('.venv', 'Scripts', 'pip.exe')
subprocess.call([vpip, 'install', '--upgrade', 'git+https://github.com/pytroll/aggdraw', 'git+https://github.com/Zulko/moviepy.git', 'numpy==1.19.3', 'pillow', 'pylint', 'scipy', 'svgwrite', 'xlrd'])
