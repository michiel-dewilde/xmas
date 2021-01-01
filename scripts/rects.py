import os
import xml.etree.ElementTree as ET

rectTag = '{http://www.w3.org/2000/svg}rect'
imageTag = '{http://www.w3.org/2000/svg}image'

class Rect:
    def __init__(self, x, y, w, h):
        x = round(x)
        y = round(y)
        w = round(w)
        h = round(h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pmin = (x, y)
        self.pmax = (x+w, y+h)
    def __repr__(self):
        return str([self.pmin, self.pmax])

class Rects:
    def __init__(self):
        self.bbox = None # bounding
        self.cbox = None # crop
        self.kbox = None # kerstversiering
        self.mbox = None # muzikant
        self.hbox = None # head

def readKeyRects():
    keyRects = {}    
    for filename in os.listdir(os.path.join('data', 'rect')):
        key, ext =  os.path.splitext(filename)
        if ext != '.svg':
            continue
        rects = Rects()
        root = ET.parse(os.path.join('data', 'rect', filename))
        for e in root.iter():
            if e.tag in (rectTag, imageTag):
                attrname = 'bbox' if e.tag == imageTag else e.attrib['id']
                setattr(rects, attrname, Rect(float(e.attrib['x']), float(e.attrib['y']), float(e.attrib['width']), float(e.attrib['height'])))
                keyRects[key] = rects
    return keyRects

keyRects = readKeyRects()