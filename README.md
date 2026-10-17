# Real-Time Ball Detection using OpenCV 🎾

A real-time computer vision prototype that detects a tennis ball through a webcam using **Python, OpenCV, and classical image processing techniques**.

The system uses HSV color segmentation, morphological filtering, contour analysis, and temporal smoothing to locate a tennis ball and visualize its position in real time.

## Features

- **Live Webcam Processing** — Captures and processes video frames in real time.
- **HSV Color Segmentation** — Isolates yellow-green tennis balls using configurable color thresholds.
- **Noise Reduction** — Uses Gaussian blur and morphological operations to improve segmentation.
- **Contour Detection** — Extracts object boundaries from the binary mask.
- **Shape Filtering** — Uses contour area and circularity to reject some false detections.
- **Position Smoothing** — Applies an Exponential Moving Average (EMA) to reduce jitter.
- **Visual Debugging** — Displays the detected contour, enclosing circle, center point, coordinates, and HSV mask.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core implementation |
| OpenCV | Image processing and object detection |
| NumPy | Array operations and numerical calculations |

## How It Works

The detection pipeline consists of seven stages:

1. **Frame Capture:** Read frames from the webcam.
2. **Preprocessing:** Apply Gaussian blur to reduce pixel-level noise.
3. **HSV Conversion:** Convert BGR frames into HSV color space.
4. **Color Segmentation:** Generate a binary mask using configurable HSV thresholds.
5. **Morphological Filtering:** Remove small noise regions and close minor gaps.
6. **Contour Analysis:** Identify candidate regions using area and circularity constraints.
7. **Detection Visualization:** Select the largest valid candidate, smooth its position and radius, and draw the result.

```text
Webcam
   |
   v
Gaussian Blur
   |
   v
BGR → HSV
   |
   v
Color Thresholding
   |
   v
Morphological Filtering
   |
   v
Contour Detection
   |
   v
Area + Circularity Filtering
   |
   v
Largest Candidate Selection
   |
   v
EMA Smoothing
   |
   v
Live Detection Visualization
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A working webcam
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Create and activate a virtual environment:

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install opencv-python numpy
```

### Run

```bash
python ball_detect.py
```

Two windows will appear:

- **Ball Detector:** Live webcam feed with detection overlays.
- **HSV Mask:** Binary visualization of pixels matching the selected color range.

Press **Q** while an OpenCV window is focused to exit.

## Configuration

The detector currently uses the following HSV thresholds for yellow-green tennis balls:

```python
lower = np.array([20, 40, 40])
upper = np.array([85, 255, 255])
```

Detection and smoothing parameters:

```python
MIN_AREA = 300
MIN_CIRCULARITY = 0.55
alpha = 0.75
```

These values are experimental and may require adjustment depending on lighting, camera quality, ball appearance, and distance.

## Current Limitations

This project is an early-stage prototype.

- Optimized primarily for yellow-green tennis balls.
- Can produce false positives from similarly colored objects.
- May struggle with shadows, occlusion, motion blur, and inconsistent lighting.
- Currently selects the largest qualifying candidate in each frame.
- EMA smoothing reduces jitter but introduces some positional lag.
- Does not yet maintain persistent object identities across frames.
- Does not yet support reliable multi-ball tracking.

## Development Roadmap

- [x] Webcam integration
- [x] HSV color segmentation
- [x] Morphological preprocessing
- [x] Contour extraction and visualization
- [x] Area and circularity filtering
- [x] Basic temporal smoothing
- [ ] Improved detection robustness
- [ ] Persistent object IDs
- [ ] Motion estimation and trajectory visualization
- [ ] Region-of-interest tracking
- [ ] Full-frame recovery when tracking is lost
- [ ] Occlusion handling
- [ ] Multi-ball tracking and counting
- [ ] Performance evaluation using recorded video

## Project Status

**Version 1.0 — Functional single-ball detection prototype**

The current implementation demonstrates real-time tennis ball detection using classical computer vision.

Future development will focus on converting independent frame-level detections into a robust tracking system capable of maintaining object identities across time.

## License

License not yet specified.
