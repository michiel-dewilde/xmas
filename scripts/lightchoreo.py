import math
import numpy as np
import scipy.interpolate
from .tempo import m2t, t2m

framerate = 30
maxlights = 1000
maxtime = 180

maxframe = framerate * maxtime

black = np.array((0,0,0))
red = np.array((1,0,0))
green = np.array((0,1,0))
blue = np.array((0,0,1))
yellow = np.array((1,1,0))
white = np.array((1,1,1))
darkblue = np.array((0,0,0.5))

rgb_lights = np.zeros([maxframe, maxlights, 3])

def add_const(i, m0, m1, rgb):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        rgb_lights[f0:f1, i::4] = np.array(rgb)

def add_change(i, m0, rgb0, m1, rgb1):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        linfit = scipy.interpolate.interp1d([m0,m1], np.vstack([np.array(rgb0), np.array(rgb1)]), axis=0)
        interpolated = linfit(t2m(np.arange(f0,f1)/framerate))
        rgb_lights[f0:f1, i::4] = interpolated[:,np.newaxis]

# 1 1
#     (ting ting ting x13)

# 4 3
#     I don't want a lot for Christmas
#     There is just one thing I need

add_change(0, 5, black, 9, green)
add_change(1, 5, black, 9, green)

# 9 2
#     I don't care about the presents
#     Underneath the Christmas tree

add_const(0, 9, 13, green)
add_const(1, 9, 13, green)
add_change(2, 9, black, 13, red)
add_change(3, 9, black, 13, red)

# 12 4
#     I just want you for my own
#     More than you could ever know

add_change(0, 13, green, 17, black)
add_change(1, 13, green, 17, black)
add_change(2, 13, red, 17, black)
add_change(3, 13, red, 17, black)

# 17 1
#     Make my wish come true

for i in range(4):
    add_change(i, 17.75, black, 18, yellow)
    add_const(i, 18, 18.5, yellow)
    add_change(i, 18.5, yellow, 19, darkblue)

# 19 1
#     All I want for Christmas is

for i in range(4):
    add_const(i, 19, 20, darkblue)
    add_change(i, 20, darkblue, 21, black)

# 21 1
#     you, yeah (ta-da-ta-da-ta-da)

np.random.seed(0)


# 25 1
#     I don't want a lot for Christmas
#     There is just one thing I need



# 29 1
#     And I don't care about the presents
#     Underneath the Christmas tree

# 32 3
#     I just want you for my own
#     More than you could ever know

# 37 1
#     Make my wish come true
#     All I want for Christmas is you
#     You, baby (ta-da-ta-da-ta-da)

# 45 1
#     Oh, all the lights are shining
#     so brightly everywhere
#     And the sound of children's
#     laughter fills the air

# 53 1
#     And everyone is singing
#     I hear those sleigh bells ringing

# 57 1
#     Santa, won't you bring me the one I really need?
#     Won't you please bring my baby to me?

# 61 1
#     Oh, I don't want a lot for Christmas
#     This is all I'm asking for

# 65 1
#     I just wanna see my baby
#    Standing right outside my door

# 68 3
#     Oh, I just want you for my own
#     More than you could ever know

# 73 1
#    Make my wish come true
#    All I want for Christmas
#    (ta-da-ta-da-ta-da)

# 79 1
#     You, baby
#     You, baby

# 87 1
#     All I want for Christmas is you, baby
#     All I want for Christmas is you

# 94 1
#     You!