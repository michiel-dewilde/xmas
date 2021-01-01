import math, os, svgwrite
from scripts.rects import keyRects as keyRects
from scripts.sheets import minputs
from PIL import Image

boxes = ['bbox', 'cbox', 'kbox', 'mbox', 'hbox']

for box in boxes:
    os.makedirs(os.path.join('data', 'clips', box), exist_ok=True)

for key, rects in keyRects.items():
    for box in boxes:
        clipfile = os.path.join('data', 'clips', box, f'{key}.png')
        srcimg = None
        if not os.path.exists(clipfile):
            if srcimg is None:
                srcimg = Image.open(os.path.join('data', 'snap', f'{key}.png'))
            rect = getattr(rects, box)
            dstimg = srcimg.crop((rect.pmin[0], rect.pmin[1], rect.pmax[0], rect.pmax[1]))
            dstimg.save(clipfile)

os.makedirs(os.path.join('data', 'arr'), exist_ok=True)

arrs = ([item[4:] for item in dir(iter(minputs.values()).__next__()) if item.startswith('arr_')])
for arr in arrs:
    arrfile = os.path.join('data', 'arr',f'{arr}.svg')
    if os.path.exists(arrfile):
        continue
    cweight = 0
    for key, minput in minputs.items():
        val = getattr(minput, f'arr_{arr}')
        if val:
            cweight += minput.weight
    size = (1920, 1080)
    dwg = svgwrite.Drawing(arrfile, profile='tiny', viewBox=(f'0 0 {size[0]} {size[1]}'))
    unitarea = size[0]*size[1]/cweight
    for key, minput in minputs.items():
        val = getattr(minput, f'arr_{arr}')
        if val:
            boxname = f'{val}box'
            rect = getattr(keyRects[key], boxname)
            area = unitarea*minput.weight
            dwg.add(dwg.image(f'../clips/{boxname}/{key}.png', insert=(0,0), size=(math.sqrt(area*rect.w/rect.h),math.sqrt(area*rect.h/rect.w)), id=key))
    dwg.save()
