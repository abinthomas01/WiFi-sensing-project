#!/usr/bin/env bash
# Launch Gazebo with the balthazar show test world (no animation)
set -e
export GAZEBO_MODEL_PATH="$PWD/assets/models:$PWD/assets"
gazebo "$PWD/assets/worlds/balthazar_show_test.world" 
