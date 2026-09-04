#!/usr/bin/env python3

import subprocess

cmd = [
    "gz",
    "topic",
    "-p",
    "/gazebo/default/pose/modify",
    "-m",
    "gazebo.msgs.Pose",
    "-e",
    """
name: "middle_age_man__rigged__animated__free"
position {
  x: -1.5
  y: -1.5
  z: 0
}
"""
]

subprocess.run(cmd)