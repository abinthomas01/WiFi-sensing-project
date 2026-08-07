#!/usr/bin/env python3

import math
import time
import subprocess

MODEL_NAME = "middle_age_man__rigged__animated__free"

x = -0.747371
y = -1.89164

TARGET_X = 1.67597
TARGET_Y = 1.00138

STEP = 0.03

while True:

    dx = TARGET_X - x
    dy = TARGET_Y - y

    dist = math.sqrt(dx * dx + dy * dy)

    if dist < 0.10:
        print("Reached Hall")
        break

    x += STEP * dx / dist
    y += STEP * dy / dist

    cmd = f"""
name: "{MODEL_NAME}"
position {{
  x: {x}
  y: {y}
  z: 0
}}
"""

    subprocess.run([
        "gz",
        "topic",
        "-p",
        "/gazebo/default/pose/modify",
        "-m",
        "gazebo.msgs.Pose",
        "-e",
        cmd
    ])

    time.sleep(0.05)