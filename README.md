# Single Board Control – Kinect Capture & Turntable Automation

This repository contains a small control system for capturing RGB and depth
images of plants from multiple angles using two Kinect v2 sensors and an
Arduino‑driven turntable.

## Overview

Components:

- `control.py` – main CLI for talking to the Arduino and orchestrating
  full capture cycles (0°, 90°, 180°, 270°).
- `camera_red.py` / `camera_green.py` – capture RGB + depth frames from
  the two Kinect devices and save them as `.jpg` + `.npy` files.
- `viewer_red.py` / `viewer_green.py` – simple live‑view utilities for
  each Kinect so you can check framing and focus.

The system expects:

- Two Kinect v2 sensors, each with its own serial number
- `libfreenect2` installed with Python bindings (`pylibfreenect2` or
  `freenect2`)
- An Arduino connected over USB (e.g. `/dev/ttyACM0`) that accepts simple
  single‑character commands to rotate and stop the platform.

## Setup

1. **Install Python dependencies** (Python 3.8+ recommended):

   ```bash
   pip install -r requirements.txt
   ```

2. **Install libfreenect2 and bindings**

   Follow the official libfreenect2 / pylibfreenect2 instructions for your
   OS. On Linux this usually means building `libfreenect2` from source,
   then installing `pylibfreenect2` for Python.

3. **Connect hardware**

   - Plug in both Kinects and confirm they show up in `lsusb` / Device
     Manager.
   - Plug in the Arduino and note the serial port (default in the code is
     `/dev/ttyACM0`).

4. **Adjust configuration (if needed)**

   - In `camera_red.py` and `camera_green.py`, update the default
     `--serial` values to match your Kinect serial numbers.
   - In `control.py`, adjust `arduino_port` in the `Host` constructor if
     your Arduino is on a different port (e.g. `COM3` on Windows).

## Usage

from the repo root:

- **Manual control loop**:

  ```bash
  python control.py
  ```

  You’ll see a prompt where you can type commands like:

  - `h` / `help` – show commands
  - `red` / `green` – rotate in either direction
  - `stop` – stop rotation
  - `capture` – run a full automated 0/90/180/270° capture sequence
  - `viewer_red` / `viewer_green` – open live view from each camera

- **Direct camera capture**:

  ```bash
  # green Kinect
  python camera_green.py 0_degrees 1

  # red Kinect
  python camera_red.py 180_degrees 1
  ```

  This will save files like:

  - `0_degrees_rgb_plant_1.jpg`
  - `0_degrees_rgb_plant_1.npy`
  - `0_degrees_depth_plant_1.jpg`
  - `0_degrees_depth_plant_1.npy`

- **Live viewer only**:

  ```bash
  python viewer_green.py
  python viewer_red.py
  ```

## Cloning & pushing to GitHub

1. Download this folder (or the zip I’ve generated in this session).
2. In a terminal:

   ```bash
   cd single_board_control_repo
   git init
   git add .
   git commit -m "Initial import of single board control project"
   git branch -M main
   git remote add origin <YOUR_GITHUB_REMOTE_URL>
   git push -u origin main
   ```

After that, you’ll be able to clone it on any compatible machine, install
the dependencies, and run the scripts as described above.
