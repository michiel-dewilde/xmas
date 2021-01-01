from scripts.rects import keyRects as keyRects

for key, value in keyRects.items():
    print(key, value.bbox, value.cbox, value.kbox, value.mbox, value.hbox)