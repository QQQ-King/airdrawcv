# -*- coding: utf-8 -*-
import argparse, time, cv2
from pathlib import Path
from src.airdrawcv.tracker import ColorTracker, PRESETS
from src.airdrawcv.airdraw import AirDrawer

BGR_COLORS = {
    "blue":   (255, 0, 0),
    "green":  (0, 255, 0),
    "red":    (0, 0, 255),
    "yellow": (0, 255, 255),
    "purple": (255, 0, 255),
    "white":  (255, 255, 255),
}

def main():
    ap = argparse.ArgumentParser(description="AirDrawCV - draw with a colored object")
    ap.add_argument("--source", default="0", help="Camera index (e.g., 0) or a video file path.")
    ap.add_argument("--preset", default="blue", choices=list(PRESETS.keys()))
    for k in ["hmin","hmax","smin","smax","vmin","vmax"]:
        ap.add_argument(f"--{k}", type=int, default=None)
    ap.add_argument("--fade", type=float, default=0.0, help="Trail fade per frame (0..1)")
    ap.add_argument("--record", action="store_true", help="Record to outputs/record.mp4")
    args = ap.parse_args()

    tracker = ColorTracker(preset=args.preset)
    custom = {k:getattr(args,k) for k in ["hmin","hmax","smin","smax","vmin","vmax"] if getattr(args,k) is not None}
    if custom: tracker.update_hsv(**custom)

    cap = cv2.VideoCapture(int(args.source)) if args.source.isdigit() else cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print("[Error] Cannot open source:", args.source); return
    ret, frame = cap.read()
    if not ret: print("[Error] Cannot read first frame."); return
    h, w = frame.shape[:2]
    drawer = AirDrawer(w, h, brush_color=BGR_COLORS["blue"], brush_size=6, fade=args.fade)

    out_writer = None
    out_dir = Path("outputs"); out_dir.mkdir(parents=True, exist_ok=True)
    show_mask = False

    while True:
        ret, frame = cap.read()
        if not ret: break
        pt, mask = tracker.centroid(frame)
        if pt is not None:
            drawer.draw_point(pt)
            cv2.circle(frame, pt, 6, (0,255,255), -1)

        vis = drawer.overlay(frame)
        cv2.putText(vis, "Keys: [b/g/r/y/p/w] color  [1/2/3] size  c=clear s=save h=mask r=rec q=quit",
                    (10, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220,220,220), 1, cv2.LINE_AA)

        if show_mask:
            m3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            vis2 = cv2.hconcat([vis, m3])
            cv2.imshow("AirDrawCV + Mask", vis2)
        else:
            cv2.imshow("AirDrawCV", vis)

        if args.record:
            if out_writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out_writer = cv2.VideoWriter(str(out_dir/"record.mp4"), fourcc, 20.0, (vis.shape[1], vis.shape[0]))
            out_writer.write(vis)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): break
        elif key == ord('h'): show_mask = not show_mask
        elif key == ord('c'): drawer.clear()
        elif key == ord('s'):
            ts = int(time.time()); fp = out_dir / f"frame_{ts}.png"; cv2.imwrite(str(fp), vis); print("[Saved]", fp)
        elif key in (ord('1'),ord('2'),ord('3')): drawer.set_size({ord('1'):4, ord('2'):8, ord('3'):14}[key])
        elif key in (ord('b'),ord('g'),ord('r'),ord('y'),ord('p'),ord('w')):
            col = {'b':"blue",'g':"green",'r':"red",'y':"yellow",'p':"purple",'w':"white"}[chr(key)]
            drawer.set_color(BGR_COLORS[col])

    cap.release()
    if out_writer is not None: out_writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
