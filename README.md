# AirDrawCV — Draw in the Air with a Colored Object (OpenCV)

Wave a **colored object** (e.g., a blue pen cap) and paint on screen. We track HSV color, find the centroid, and draw smooth strokes on a canvas overlay. Fun, simple, and perfect for a high school CV project.

Repo target: https://github.com/YOUR_NAME/airdrawcv

## Features
- Real-time **HSV color tracking** + largest contour + centroid
- Virtual canvas with **smooth strokes** and optional **trail fade**
- **Hotkeys**: colors, sizes, clear (`c`), save (`s`), toggle mask (`h`), record (`r`), quit (`q`)
- Use webcam (`--source 0`) or video file

## Install
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python app.py --source 0 --preset blue
# or custom HSV range:
python app.py --source 0 --hmin 90 --hmax 130 --smin 80 --smax 255 --vmin 80 --vmax 255
```

## Keys
- `q` quit | `h` toggle mask | `c` clear | `s` save PNG | `r` start/stop MP4 record
- `1/2/3` brush size | `b/g/r/y/p/w` brush color

## Structure
```
airdrawcv/
 ├─ src/airdrawcv/tracker.py     # HSV tracker (mask + centroid)
 ├─ src/airdrawcv/airdraw.py     # Canvas drawing + overlay
 ├─ app.py                       # Runner + hotkeys + recording
 ├─ tests/test_synthetic.py      # Synthetic unit test
 ├─ examples/
 ├─ requirements.txt, README.md, LICENSE
```

## Push to GitHub
```bash
git init
git add .
git commit -m "Init: AirDrawCV (OpenCV color-object air drawing)"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/airdrawcv.git
git push -u origin main
```
