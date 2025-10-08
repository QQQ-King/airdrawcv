# -*- coding: utf-8 -*-
import cv2, numpy as np
from src.airdrawcv.tracker import ColorTracker
from src.airdrawcv.airdraw import AirDrawer

def test_synthetic_path():
    h, w = 240, 320
    tr = ColorTracker(preset="blue")
    dr = AirDrawer(w, h, brush_size=4)
    for x in range(20, 220, 12):
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        cv2.circle(frame, (x, 120), 12, (255,0,0), -1)  # blue (BGR)
        pt, _ = tr.centroid(frame, min_area=10)
        if pt is not None:
            dr.draw_point(pt)
    out = dr.overlay(np.zeros((h,w,3), dtype=np.uint8))
    assert int(out.sum()) > 0
