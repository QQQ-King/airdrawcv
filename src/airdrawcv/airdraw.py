# -*- coding: utf-8 -*-
import cv2
import numpy as np

class AirDrawer:
    def __init__(self, width, height, brush_color=(255,0,0), brush_size=6, fade=0.0):
        self.canvas = np.zeros((height, width, 4), dtype=np.uint8)  # RGBA
        self.prev_pt = None
        self.color = brush_color
        self.size = int(brush_size)
        self.fade = float(fade)

    def set_color(self, bgr): self.color = bgr
    def set_size(self, s): self.size = int(max(1, s))
    def clear(self): self.canvas[:] = 0; self.prev_pt = None

    def draw_point(self, pt):
        if self.fade > 0:
            alpha = max(0.0, 1.0 - self.fade)
            self.canvas = (self.canvas.astype(np.float32) * alpha).astype(np.uint8)
        if self.prev_pt is None:
            self.prev_pt = pt; return
        cv2.line(self.canvas, self.prev_pt, pt, color=(*self.color, 255), thickness=self.size, lineType=cv2.LINE_AA)
        self.prev_pt = pt

    def overlay(self, frame_bgr):
        out = frame_bgr.copy()
        a = self.canvas[:,:,3:4] / 255.0
        out = (out*(1-a) + self.canvas[:,:,:3]*a).astype(np.uint8)
        return out
