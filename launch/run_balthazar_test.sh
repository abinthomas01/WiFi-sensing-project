#!/usr/bin/env bash
# Launch script to run the balthazar walk test world with Gazebo
# Sets GZ resource path to include project assets
PROJECT_ROOT="$HOME/Projects/wifi_sensing_ros2"
export GZ_SIM_RESOURCE_PATH="$PROJECT_ROOT/assets:$GZ_SIM_RESOURCE_PATH"

# Try ignition gazebo first (common on newer setups), fall back to classic gazebo
if command -v ign >/dev/null 2>&1; then
  echo "Launching ign gazebo with test world"
  ign gazebo "$PROJECT_ROOT/assets/worlds/balthazar_walk_test.world"
else
  echo "Launching classic gazebo with test world"
  gazebo "$PROJECT_ROOT/assets/worlds/balthazar_walk_test.world"
fi
