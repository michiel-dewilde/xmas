#!/bin/sh
ffmpeg -i xmas-master.wav -af ebur128=framelog=verbose -f null - 2>&1 | awk '/I:/{print $2}'
