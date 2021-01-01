import subprocess, os, sys
if not os.path.exists('.venv'):
    subprocess.call([sys.executable, '-m', 'venv', '.venv'])
vpy = os.path.join('.venv', 'Scripts', 'python.exe')
subprocess.call([vpy, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
vpip = os.path.join('.venv', 'Scripts', 'pip.exe')
subprocess.call([vpip, 'install', '--upgrade', 'aggdraw', 'numpy==1.19.3', 'pillow', 'pylint', 'scipy', 'moviepy'])
