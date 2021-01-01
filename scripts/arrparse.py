import math, re, os
import xml.etree.ElementTree as ET

groupTag = '{http://www.w3.org/2000/svg}g'
imageTag = '{http://www.w3.org/2000/svg}image'

class Bbox:
    def __init__(self, pmin = None, pmax = None):        
        #print(pmin, pmax)
        self.pmin = pmin if pmin else (math.inf, math.inf)
        self.pmax = pmax if pmax else (-math.inf, -math.inf)
        self.center = (math.nan, math.nan) if (pmin == None and pmax == None) else ((pmin[0]+pmax[0])/2, (pmin[1]+pmax[1])/2)
        assert (pmin == None and pmax == None) or (math.isfinite(self.center[0]) and math.isfinite(self.center[1]))
    def __add__(self, other):
        #print(self.pmin, self.pmax, other.pmin, other.pmax)
        #print(min(math.inf, 0))
        return Bbox((min(self.pmin[0], other.pmin[0]), min(self.pmin[1], other.pmin[1])), (max(self.pmax[0], other.pmax[0]), max(self.pmax[1], other.pmax[1])))
    def translated(self, p):
        return Bbox((self.pmin[0]+p[0], self.pmin[1]+p[1]), (self.pmax[0]+p[0], self.pmax[1]+p[1]))

def get_translation(node):
    if 'transform' not in node.attrib or not node.attrib['transform']:
        return (0,0)
    else:
        m = re.match(r'^[ ]*translate\([ ]*([-0-9.eE]+)[ ]*,[ ]*([-0-9.eE]+)[ ]*\)[ ]*$', node.attrib['transform'])
        assert m
        return (float(m.group(1)), float(m.group(2)))

class Cluster:
    def __init__(self, indices = [], bbox = Bbox()):
        self.indices = indices
        self.bbox = bbox

class Partial_layout:
    def __init__(self, node):
        if node.tag == imageTag:
            x = float(node.attrib['x'])
            y = float(node.attrib['y'])
            w = float(node.attrib['width'])
            h = float(node.attrib['height'])
            self.bbox = Bbox((x,y), (x+w,y+h))
            self.layout = node.attrib['id']
        else:
            partial_layouts = [Partial_layout(e) for e in node if e.tag in [groupTag, imageTag]]
            assert partial_layouts
            self.bbox = Bbox()
            for partial_layout in partial_layouts:
                self.bbox = self.bbox + partial_layout.bbox
            #print(self.bbox)
            h_clusters = [Cluster([i], partial_layouts[i].bbox) for i in range(len(partial_layouts))]
            v_clusters = [Cluster([i], partial_layouts[i].bbox) for i in range(len(partial_layouts))]
            while len(h_clusters)*len(v_clusters) > len(partial_layouts):
                #print("A", len(h_clusters), len(v_clusters), len(partial_layouts))
                win_cost = math.inf
                win_clusters = None
                win_i = None
                win_j = None
                for i in range(len(h_clusters)):
                    for j in range(i + 1, len(h_clusters)):
                        cost = abs(h_clusters[i].bbox.center[1] - h_clusters[j].bbox.center[1])
                        #print("Ch",cost,win_cost)
                        if cost < win_cost:
                            win_cost = cost
                            win_clusters = h_clusters
                            win_i = i
                            win_j = j
                for i in range(len(v_clusters)):
                    for j in range(i + 1, len(v_clusters)):
                        cost = abs(v_clusters[i].bbox.center[0] - v_clusters[j].bbox.center[0])
                        #print("Cv",cost,win_cost)
                        if cost < win_cost:
                            win_cost = cost
                            win_clusters = v_clusters
                            win_i = i
                            win_j = j
               # print("B", i, j)
                win_clusters[win_i].indices += win_clusters[win_j].indices
                win_clusters[win_i].bbox = win_clusters[win_i].bbox + win_clusters[win_j].bbox
                del win_clusters[win_j]
            assert len(h_clusters)*len(v_clusters) == len(partial_layouts), node.attrib['id']
            assert min([len(cluster.indices) for cluster in h_clusters]) == max([len(cluster.indices) for cluster in h_clusters])
            assert min([len(cluster.indices) for cluster in v_clusters]) == max([len(cluster.indices) for cluster in v_clusters])
            if len(v_clusters) > 1:
                v_clusters = sorted(v_clusters, key=lambda cluster: cluster.bbox.center[0])
                h_layouts = []
                for cluster in v_clusters:
                    if len(cluster.indices) == 1:
                        h_layouts.append(partial_layouts[cluster.indices[0]].layout)
                    else:
                        h_layouts.append({'v': [partial_layouts[i].layout for i in sorted(cluster.indices, key = lambda i: partial_layouts[i].bbox.center[1])]})
                self.layout = {'h': h_layouts}
            elif len(h_clusters) > 1:
                h_clusters = sorted(h_clusters, key=lambda cluster: cluster.bbox.center[1])
                self.layout = {'v': [partial_layouts[cluster.indices[0]].layout for cluster in h_clusters]}
            elif partial_layouts:
                self.layout = partial_layouts[0].layout
            else:
                assert False, f"no content in node {node.attrib['id']}"
        self.bbox = self.bbox.translated(get_translation(node))

def get_arr_layout(key):
    root = ET.parse(os.path.join('data', 'arr', f'{key}.svg')).getroot()
    return Partial_layout(root).layout
