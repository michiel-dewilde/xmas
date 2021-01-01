import random
import colorsys, math
import numpy as np
import scipy.interpolate
import scipy.signal
from .tempo import m2t, t2m
from .common import *

framerate = 30
maxlights = 1000
maxtime = 200

maxframe = framerate * maxtime

black = np.array((0,0,0))
red = np.array((1,0,0))
green = np.array((0,1,0))
blue = np.array((0,0,1))
yellow = np.array((1,1,0))
brightyellow = np.array((1,1,0.75))
white = np.array((1,1,1))
darkblue = np.array((0,0,0.5))

darkred = red / 2
darkgreen = green / 2

hsv2rgb = np.vectorize(lambda col: np.array(colorsys.hsv_to_rgb(col[0], col[1], col[2])), signature='(3)->(3)')
rgb2hsv = np.vectorize(lambda col: np.array(colorsys.rgb_to_hsv(col[0], col[1], col[2])), signature='(3)->(3)')

choreo = np.zeros([maxframe, maxlights, 3])

def add_const(i, m0, m1, rgb):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        choreo[f0:f1, i::4] = np.array(rgb)

def add_change(i, m0, rgb0, m1, rgb1):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        linfit = scipy.interpolate.interp1d([m0,m1], np.stack([np.array(rgb0), np.array(rgb1)]), axis=0)
        interpolated = linfit(t2m(np.arange(f0,f1)/framerate))
        choreo[f0:f1, i::4] = interpolated[:,np.newaxis]

def add_all_const(m0, m1, rgb):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        choreo[f0:f1, :] = np.array(rgb)

def add_all_change(m0, rgb0, m1, rgb1):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        linfit = scipy.interpolate.interp1d([m0,m1], np.stack([np.array(rgb0), np.array(rgb1)]), axis=0)
        interpolated = linfit(t2m(np.arange(f0,f1)/framerate))
        choreo[f0:f1, :] = interpolated[:,np.newaxis]

def add_array_const(i, m0, m1, rgb):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        choreo[f0:f1, i::4] = rgb[np.newaxis, :]

def add_array_change(i, m0, rgb0, m1, rgb1):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        linfit = scipy.interpolate.interp1d([m0,m1], np.stack([rgb0, rgb1]), axis=0)
        interpolated = linfit(t2m(np.arange(f0,f1)/framerate))
        choreo[f0:f1, i::4] = interpolated[:,:]

def add_all_array_const(m0, m1, rgb):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        choreo[f0:f1, :] = rgb[np.newaxis, :]

def add_all_array_change(m0, rgb0, m1, rgb1):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        linfit = scipy.interpolate.interp1d([m0, m1], np.stack([rgb0, rgb1]), axis=0)
        interpolated = linfit(t2m(np.arange(f0,f1)/framerate))
        choreo[f0:f1, :] = interpolated[:,:]

def rand_bright_color_array(nlights):
    c = np.empty((nlights, 3))
    c[:, 0] = np.random.rand(nlights)
    c[:, 1] = 1
    c[:, 2] = 1
    c[:] = hsv2rgb(c[:])
    return c

# 1 1
#     (ting ting ting x13)

# 4 3
#     I don't want a lot for Christmas
#     There is just one thing I need

add_change(0, 5, black, 9, red)
add_change(1, 5, black, 9, red)

# 9 2
#     I don't care about the presents
#     Underneath the Christmas tree

add_const(0, 9, 13, red)
add_const(1, 9, 13, red)
add_change(2, 9, black, 13, green)
add_change(3, 9, black, 13, green)

# 12 4
#     I just want you for my own
#     More than you could ever know

add_change(0, 13, red, 17, black)
add_change(1, 13, red, 17, black)
add_change(2, 13, green, 17, black)
add_change(3, 13, green, 17, black)

# 17 1
#     Make my wish come true

for i in range(4):
    add_change(i, 17.75, black, 18, brightyellow)
    add_const(i, 18, 18.5, brightyellow)
    add_change(i, 18.5, brightyellow, 19, darkblue)

# 19 1
#     All I want for Christmas is

for i in range(4):
    add_const(i, 19, 20, darkblue)
    add_change(i, 20, darkblue, 21, black)

# 21 1
#     you, yeah (ta-da-ta-da-ta-da)

add_all_change(21, black, 22, red)
add_all_change(22, black, 23, green)
add_all_change(23, black, 24, yellow)

for b in range(3):
    add_all_const(24+(b + 4/6)/4, 24+(b + 5/6)/4, brightyellow)
    add_all_const(24+(b + 1)/4, 24+(b + 1 + 2/6)/4, brightyellow)

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

for m in range(25,45):
    c = rand_bright_color_array(maxlights)
    add_array_const(0, m, m+0.25, c[0::4])
    add_array_const(1, m, m+0.25, c[1::4])
    add_array_const(2, m+0.25, m+0.5, c[2::4])
    add_array_const(3, m+0.25, m+0.5, c[3::4])
    c = rand_bright_color_array(maxlights)
    add_array_const(0, m+0.5, m+0.75, c[0::4])
    add_array_const(1, m+0.5, m+0.75, c[1::4])
    add_array_const(2, m+0.75, m+1, c[2::4])
    add_array_const(3, m+0.75, m+1, c[3::4])

# 45 1
#     Oh, all the lights are shining
#     so brightly everywhere

add_change(1, 45, black, 46, red)
add_const(1, 46, 47, red)
add_change(1, 47, red, 48, black)
add_change(2, 46, black, 47, green)
add_const(2, 47, 48, green)
add_change(2, 48, green, 49, black)

for m in range(45,49):
    c = rand_bright_color_array(maxlights)/2
    add_array_const(0, m, m+0.25, c[0::4])
    add_array_const(3, m+0.25, m+0.5, c[3::4])
    c = rand_bright_color_array(maxlights)/2
    add_array_const(0, m+0.5, m+0.75, c[0::4])
    add_array_const(3, m+0.75, m+1, c[3::4])

# 49 1
#     And the sound of children's
#     laughter fills the air

add_change(1, 49, black, 50, red)
add_const(1, 50, 51, red)
add_change(1, 51, red, 52, black)
add_change(2, 50, black, 51, green)
add_const(2, 51, 52, green)
add_change(2, 52, green, 53, black)

for m in range(49,53):
    c = rand_bright_color_array(maxlights)/2
    add_array_const(0, m, m+0.25, c[0::4])
    add_array_const(3, m+0.25, m+0.5, c[3::4])
    c = rand_bright_color_array(maxlights)/2
    add_array_const(0, m+0.5, m+0.75, c[0::4])
    add_array_const(3, m+0.75, m+1, c[3::4])

# 53 1
#     And everyone is singing
#     I hear those sleigh bells ringing

add_change(1, 53, black, 55, darkblue)
add_change(2, 53, black, 55, darkblue)
add_change(1, 55, darkblue, 57, yellow)
add_change(2, 55, darkblue, 57, yellow)

for m in range(53,57):
    c = rand_bright_color_array(maxlights)/2
    add_array_const(0, m, m+0.25, c[0::4])
    add_array_const(3, m+0.25, m+0.5, c[3::4])
    c = rand_bright_color_array(maxlights)/2
    add_array_const(0, m+0.5, m+0.75, c[0::4])
    add_array_const(3, m+0.75, m+1, c[3::4])

# 57 1
#     Santa, won't you bring me the one I really need?
#     Won't you please bring my baby to me?

add_all_const(57, 57+5/12, red)
add_all_const(57+5/12, 57+6/8, green)
add_all_const(57+6/8, 57+8/8, yellow)

add_all_const(58, 58+5/12, red)
add_all_const(58+5/12, 58+6/8, green)
add_const(0, 58+6/8, 58+8/8, yellow)
add_const(1, 58+6/8, 58+8/8, yellow)
add_const(2, 58+6/8, 59+1/4, yellow)
add_const(3, 58+6/8, 59+1/4, yellow)

add_const(0, 59, 59+4/8, red)
add_const(1, 59, 59+4/8, red)
add_const(2, 59+1/4, 59+11/12, red)
add_const(3, 59+1/4, 59+11/12, red)
add_const(0, 59+4/8, 59+11/12, green)
add_const(1, 59+4/8, 59+11/12, green)
add_all_const(59+11/12, 59+8/8, yellow)

add_all_array_change(60, np.broadcast_to(yellow[np.newaxis,:], (maxlights, 3)), 61, np.zeros((maxlights, 3)))

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

for m in range(61,76):
    c = rand_bright_color_array(maxlights)
    add_array_const(0, m, m+0.25, c[0::4])
    add_array_const(1, m, m+0.25, c[1::4])
    add_array_const(2, m+0.25, m+0.5, c[2::4])
    add_array_const(3, m+0.25, m+0.5, c[3::4])
    c = rand_bright_color_array(maxlights)
    add_array_const(0, m+0.5, m+0.75, c[0::4])
    add_array_const(1, m+0.5, m+0.75, c[1::4])
    add_array_const(2, m+0.75, m+1, c[2::4])
    add_array_const(3, m+0.75, m+1, c[3::4])

c = rand_bright_color_array(maxlights)
add_array_const(0, 76, 76+0.25, c[0::4])
add_array_const(1, 76, 76+0.25, c[1::4])
add_all_array_change(76.25, c, 77, np.zeros((maxlights, 3)))
add_all_array_change(77, np.zeros((maxlights, 3)), 78, c)

for b in range(3):
    add_all_const(78+(b + 4/6)/4, 78+(b + 5/6)/4, brightyellow)
    add_all_const(78+(b + 1)/4, 78+(b + 1 + 2/6)/4, brightyellow)

# 79 1
#     You, baby
#     You, baby

# 87 1
#     All I want for Christmas is you, baby
#     All I want for Christmas is you

for m in range(79,94):
    c = rand_bright_color_array(maxlights)
    add_array_const(0, m, m+0.25, c[0::4])
    add_array_const(1, m, m+0.25, c[1::4])
    add_array_const(2, m+0.25, m+0.5, c[2::4])
    add_array_const(3, m+0.25, m+0.5, c[3::4])
    c = rand_bright_color_array(maxlights)
    add_array_const(0, m+0.5, m+0.75, c[0::4])
    add_array_const(1, m+0.5, m+0.75, c[1::4])
    add_array_const(2, m+0.75, m+1, c[2::4])
    add_array_const(3, m+0.75, m+1, c[3::4])

# 94 1
#     You!

add_const(0, 94+3/12, 94+7/12, red)
add_const(1, 94+3/12, 94+7/12, red)
add_const(2, 94+5/12, 94+9/12, green)
add_const(3, 94+5/12, 94+9/12, green)
add_const(0, 94+9/12, 94+12/12, red)
add_const(1, 94+9/12, 94+12/12, red)
add_const(2, 94+11/12, 95, green)
add_const(3, 94+11/12, 95, green)

add_array_change(0, 95, np.broadcast_to(darkred[np.newaxis,:], (maxlights//4, 3)), 95+3/4,  np.broadcast_to(red[np.newaxis,:], (maxlights//4, 3)))
add_array_change(1, 95, np.broadcast_to(darkred[np.newaxis,:], (maxlights//4, 3)), 95+3/4,  np.broadcast_to(red[np.newaxis,:], (maxlights//4, 3)))
add_array_change(2, 95, np.broadcast_to(darkgreen[np.newaxis,:], (maxlights//4, 3)), 95+3/4,  np.broadcast_to(green[np.newaxis,:], (maxlights//4, 3)))
add_array_change(3, 95, np.broadcast_to(darkgreen[np.newaxis,:], (maxlights//4, 3)), 95+3/4,  np.broadcast_to(green[np.newaxis,:], (maxlights//4, 3)))

#add_all_const(95+3/4, 95+10/12, brightyellow)
#add_all_const(95+11/12, 96, brightyellow)

add_all_const(95+3/4, 95+3.25/4, brightyellow)
add_all_const(95+3.5/4, 96, brightyellow)

yeloframe = math.ceil(framerate*(m2t(96) + 5))
endperiod = 1
endperiodframes = endperiod * framerate
sine = np.tile(np.sin(np.linspace(0, 2*np.pi, endperiodframes+1))[:-1], math.ceil((maxframe-yeloframe+endperiodframes)/framerate))
for i in range(maxlights):
    offset = random.randrange(endperiodframes)
    choreo[yeloframe:,i] = yellow + np.outer((1 + sine[offset:offset + maxframe - yeloframe])/ 2, brightyellow - yellow)
endlightson = 5
endlightsonframes = endlightson * framerate
choreo[yeloframe:yeloframe+endlightsonframes,:] = np.linspace(0, 1, endlightsonframes+1)[:-1,np.newaxis,np.newaxis] * choreo[yeloframe:yeloframe+endlightsonframes,:]

def add_all_const(m0, m1, rgb):
    f0 = math.ceil(framerate * m2t(m0))
    f1 = math.ceil(framerate * m2t(m1))
    if f0 < f1:
        choreo[f0:f1, :] = np.array(rgb)

#kern = np.full(3, 1/3)
kern = np.array([0.25, 0.5, 0.25])
for light in range(maxlights):
    for rgb in range(3):
        choreo[:, light, rgb] = scipy.signal.convolve(choreo[1:maxframe, light, rgb], kern)[:maxframe]