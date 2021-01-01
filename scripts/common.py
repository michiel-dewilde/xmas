import aggdraw, colorsys, math, os, random
from PIL import Image, ImageDraw
import numpy as np
import scipy.stats as st

def gkern1d(kernlen, nsig):
    x = np.linspace(-nsig, nsig, kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    return kern1d/kern1d.sum()

def gkern2d(kernlen, nsig):
    x = np.linspace(-nsig, nsig, kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kern2d = np.outer(kern1d, kern1d)
    return kern2d/kern2d.sum()

def copy_paste_rgba(src, dst, box=None):
    srcnoalpha = src.copy()
    srcnoalpha.putalpha(255)
    dst.paste(srcnoalpha, box=box, mask=src)
    
def alpha_composite_rgba(src, dst, box=None):
    dst.alpha_composite(src, dest=((0,0) if box is None else box))