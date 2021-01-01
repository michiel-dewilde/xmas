from .rects import Rect

def wh_around(media_wh, aspect_wh):
    mw, mh = media_wh
    aw, ah = aspect_wh
    if mw * ah < mh * aw:
        h = mh
        w = mh * aw / ah
    else:
        w = mw
        h = mw * ah / aw
    return w, h

def wh_inside(media_wh, aspect_wh):
    mw, mh = media_wh
    aw, ah = aspect_wh
    if mw * ah < mh * aw:
        w = mw
        h = mw * ah / aw
    else:
        h = mh
        w = mh * aw / ah
    return w, h

class Cropdata:
    # src: source (width, height)
    # scene: source scene Rect
    # head: source head Rect
    # dst: destination (width, height)
    # inset: destination useful inset Rect
    def __init__(self, src, scene, head, dst, inset):
        print('')
        print('src: ', src)
        print('scene: ', scene)
        print('head: ', head)
        print('dst: ', dst)
        print('inset: ', inset)

        ascene_w, ascene_h = wh_around(media_wh = (scene.w, scene.h), aspect_wh = (inset.w, inset.h))
        scene_cx = scene.x + scene.w/2
        scene_cy = scene.y + scene.h/2
        ascale = ascene_w / inset.w
        l = max(scene_cx/2 - ascene_w/2 - ascale * inset.pmin[0], 0)
        t = max(scene_cy/2 - ascene_h/2 - ascale * inset.pmin[1], 0)
        r = min(scene_cx/2 + ascene_w/2 + ascale * (dst[0] - inset.pmax[0]), src[0])
        b = min(scene_cy/2 + ascene_h/2 + ascale * (dst[1] - inset.pmax[1]), src[1])
        iscene_w, iscene_h = wh_inside(media_wh = (r - l, b - t), aspect_wh = (dst[0], dst[1]))
        iscale = iscene_w / dst[0]

        phead_l = head.pmin[0] - iscale * inset.pmin[0]
        phead_t = head.pmin[1] - iscale * inset.pmin[1]
        phead_r = head.pmax[0] + iscale * (dst[0] - inset.pmax[0])
        phead_b = head.pmax[1] + iscale * (dst[1] - inset.pmax[1])

        work_l = scene_cx - iscene_w / 2
        work_t = scene_cy - iscene_h / 2
        work_r = scene_cx + iscene_w / 2
        work_b = scene_cy + iscene_h / 2

        if phead_r - phead_l > work_r - work_l:
            head_cx = (phead_l + phead_r)  / 2
            work_l = head_cx - iscene_w / 2
            work_r = head_cx + iscene_w / 2
        elif phead_l < work_l:
            work_l = phead_l
            work_r = phead_l + iscene_w
        elif phead_r > work_r:
            work_r = phead_r
            work_l = phead_r - iscene_w

        if phead_b - phead_t > work_b - work_t:
            head_cy = (phead_t + phead_b) / 2
            work_t = head_cy - iscene_h / 2
            work_b = head_cy + iscene_h / 2
        elif phead_t < work_t:
            work_t = phead_t
            work_b = phead_t + iscene_h
        elif phead_b > work_b:
            work_b = phead_b
            work_t = phead_b - iscene_h

        self.size = (max(round(src[0] / iscale), dst[0]), max(round(src[1] / iscale), dst[1]))

        print('')
        print('iscene_w: ', iscene_w)
        print('iscene_h: ', iscene_h)
        print('iscale: ', iscale)

        new_w = min(round(iscene_w / iscale), self.size[0])
        new_h = min(round(iscene_h / iscale), self.size[1])
        new_x = round(work_l / iscale)
        new_y = round(work_t / iscale)

        if new_x < 0:
            new_x = 0
        elif new_x + new_w > self.size[0]:
            new_x = self.size[0] - new_w

        if new_y < 0:
            new_y = 0
        elif new_y + new_h > self.size[1]:
            new_y = self.size[1] - new_h

        self.crop = Rect(new_x, new_y, new_w, new_h)
        print('')
        print('size: ', self.size)
        print('crop: ', self.crop)
