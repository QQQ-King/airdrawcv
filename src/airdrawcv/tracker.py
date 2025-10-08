# -*- coding: utf-8 -*-
import cv2
import numpy as np

PRESETS = {
    "blue":   dict(hmin=90,  hmax=130, smin=80,  smax=255, vmin=80,  vmax=255),
    "green":  dict(hmin=40,  hmax=85,  smin=60,  smax=255, vmin=70,  vmax=255),
    "red":    dict(hmin=0,   hmax=10,  smin=80,  smax=255, vmin=80,  vmax=255),
    "yellow": dict(hmin=20,  hmax=35,  smin=80,  smax=255, vmin=80,  vmax=255),
}

class ColorTracker:
    def __init__(self, hsv_range=None, preset="blue"):
        if hsv_range is None:
            hsv_range = PRESETS.get(preset, PRESETS["blue"]).copy()
        self.hsv = hsv_range

    def update_hsv(self, **kwargs):
        self.hsv.update({k: int(v) for k, v in kwargs.items() if k in self.hsv})

    def mask(self, frame_bgr):
        hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        lo = np.array([self.hsv["hmin"], self.hsv["smin"], self.hsv["vmin"]], dtype=np.uint8)
        hi = np.array([self.hsv["hmax"], self.hsv["smax"], self.hsv["vmax"]], dtype=np.uint8)
        m = cv2.inRange(hsv, lo, hi)
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k, iterations=1)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k, iterations=1)
        return m

    def centroid(self, frame_bgr, min_area=300):
        m = self.mask(frame_bgr)
        cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            return None, m
        c = max(cnts, key=cv2.contourArea)
        if cv2.contourArea(c) < min_area:
            return None, m
        M = cv2.moments(c)
        if M["m00"] == 0:
            return None, m
        cx = int(M["m10"]/M["m00"]); cy = int(M["m01"]/M["m00"])
        return (cx, cy), m
