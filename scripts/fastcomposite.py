import numpy as np

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.video.VideoClip import ColorClip, VideoClip

#adjusted from moviepy CompositeVideoClip

class FastCompositeVideoClip(VideoClip):

    """
    A VideoClip made of other videoclips displayed together. This is the
    base class for most compositions.

    Parameters
    ----------

    size
      The size (width, height) of the final clip.

    clips
      A list of videoclips.

      Clips with a higher ``layer`` attribute will be dislayed
      on top of other clips in a lower layer.
      If two or more clips share the same ``layer``,
      then the one appearing latest in ``clips`` will be displayed
      on top (i.e. it has the higher layer).

      For each clip:

      - The attribute ``pos`` determines where the clip is placed.
          See ``VideoClip.set_pos``
      - The mask of the clip determines which parts are visible.

      Finally, if all the clips in the list have their ``duration``
      attribute set, then the duration of the composite video clip
      is computed automatically

    bg_color
      Color for the unmasked and unfilled regions. Set to None for these
      regions to be transparent (will be slower).

    use_bgclip
      Set to True if the first clip in the list should be used as the
      'background' on which all other clips are blitted. That first clip must
      have the same size as the final clip. If it has no transparency, the final
      clip will have no mask.

    The clip with the highest FPS will be the FPS of the composite clip.

    """

    def __init__(
        self, clips, size=None, bg_color=None, use_bgclip=False, is_mask=False
    ):

        if size is None:
            size = clips[0].size

        if use_bgclip and (clips[0].mask is None):
            transparent = False
        else:
            transparent = bg_color is None

        if bg_color is None:
            bg_color = 0.0 if is_mask else (0, 0, 0)

        fpss = [clip.fps for clip in clips if getattr(clip, "fps", None)]
        self.fps = max(fpss) if fpss else None

        VideoClip.__init__(self)

        self.size = size
        self.is_mask = is_mask
        self.clips = clips
        self.bg_color = bg_color

        if use_bgclip:
            self.bg = clips[0]
            self.clips = clips[1:]
            self.created_bg = False
        else:
            self.clips = clips
            self.bg = ColorClip(size, color=self.bg_color, is_mask=is_mask)
            self.created_bg = True

        # order self.clips by layer
        self.clips = sorted(self.clips, key=lambda clip: clip.layer)

        # compute duration
        ends = [clip.end for clip in self.clips]
        if None not in ends:
            duration = max(ends)
            self.duration = duration
            self.end = duration

        # compute audio
        audioclips = [v.audio for v in self.clips if v.audio is not None]
        if audioclips:
            self.audio = CompositeAudioClip(audioclips)

        # compute mask if necessary
        if transparent:
            maskclips = [
                (clip.mask if (clip.mask is not None) else clip.add_mask().mask)
                .with_position(clip.pos)
                .with_end(clip.end)
                .with_start(clip.start, change_end=False)
                .with_layer(clip.layer)
                for clip in self.clips
            ]

            self.mask = FastCompositeVideoClip(
                maskclips, self.size, is_mask=True, bg_color=0.0
            )

    def make_frame(self, t):
        """The clips playing at time `t` are blitted over one another."""

        #frame = self.bg.get_frame(t).astype("uint8")
        #im = Image.fromarray(frame)

        #if self.bg.mask is not None:
        #    frame_mask = self.bg.mask.get_frame(t)
        #    im_mask = Image.fromarray(255 * frame_mask).convert("L")
        #    im = im.putalpha(im_mask)

        #for clip in self.playing_clips(t):
        #    im = clip.blit_on(im, t)

        #return np.array(im)

        im = np.zeros((self.size[1], self.size[0], 3), dtype='uint8')
        for clip in self.playing_clips(t):
            ct = t - clip.start
            pos = clip.pos(ct)
            frame = clip.get_frame(ct)
            fh = frame.shape[0]
            fw = frame.shape[1]
            if clip.mask is None:
                im[pos[1]:pos[1]+fh,pos[0]:pos[0]+fw,:] = frame
            else:
                if getattr(clip,'isfixedmask',False):
                    if not hasattr(clip,'fixedmask'):
                        clip.fixedmask = (255*clip.mask.get_frame(ct)).astype('uint16')
                    mask = clip.fixedmask
                else:
                    mask = (255*clip.mask.get_frame(ct)).astype('uint16')
                framei = frame.astype('uint16')
                dsti = im[pos[1]:pos[1]+fh,pos[0]:pos[0]+fw,:].astype('uint16')
                im[pos[1]:pos[1]+fh,pos[0]:pos[0]+fw,:] = (((255-mask)[:,:,np.newaxis]*dsti + mask[:,:,np.newaxis]*framei + 127)//255).astype('uint8')
                #print(np.sum(framei), np.sum(mask), np.sum(dst), np.sum(im[pos[1]:pos[1]+fh,pos[0]:pos[0]+fw,:]))
        return im
                #if self.bg.mask is not None:
        #    frame_mask = self.bg.mask.get_frame(t)

    def playing_clips(self, t=0):
        """Returns a list of the clips in the composite clips that are
        actually playing at the given time `t`."""
        return [clip for clip in self.clips if clip.is_playing(t)]

    def close(self):
        if self.created_bg and self.bg:
            # Only close the background clip if it was locally created.
            # Otherwise, it remains the job of whoever created it.
            self.bg.close()
            self.bg = None
        if hasattr(self, "audio") and self.audio:
            self.audio.close()
            self.audio = None