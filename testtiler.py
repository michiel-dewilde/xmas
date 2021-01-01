import json
from scripts.tiler import Tiling

#tiling = Tiling(size = (1920,1080), layout = json.loads('{"h":[{"v":["a","a","a"]},{"v":["a","a"]}]}'), weights = {'a': 1.0})
tiling = Tiling(size = (1920,1080), layout = json.loads('{"ccw":{"a":1,"c":"a","d":["a","a","a","a"]}}'), weights = {'a': 1.0})

print(len(tiling.fvs))

#from pprint import pprint
for tile in tiling.tiles:
    print(tile.id, tile.tishe.pmin, tile.bishe.pmax)