import os, sys, svgwrite
from scripts import partitioning
from scripts.sheets import minputs
from scripts.partitioning import Partitioning
from scripts.arrparse import get_arr_layout

svgfile = os.path.join('media', 'end.svg')
if os.path.exists(svgfile):
    print(f'File {svgfile} already exists')
    sys.exit(-1)

weights = {}
size = (2*1920, 2*1080)
for mkey, minput in minputs.items():
    weights[mkey] = minput.weight
layout = get_arr_layout('11')
part = Partitioning(size=size, layout=layout, weights=weights)

dwg = svgwrite.Drawing(svgfile, profile='tiny', viewBox=(f'0 0 {size[0]} {size[1]}'))

clips = []
for tile in part.tiling.tiles:
    id = tile.id
    pmin = tile.tishe.pmin
    pmax = tile.bishe.pmax
    dwg.add(dwg.rect(insert=(pmin[0],pmin[1]), size=(pmax[0]-pmin[0],pmax[1]-pmin[1]), id=id, fill='none', stroke=svgwrite.rgb(0,0,0,'%'), stroke_width=4))

dwg.save()
