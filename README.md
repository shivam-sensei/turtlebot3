# TurtleBot3 Navigation2 & SLAM Workspace

A unified ROS 2 workspace for simulating the [ROBOTIS TurtleBot3](https://github.com/shivam-sensei/turtlebot3) in Gazebo and running autonomous navigation with **Nav2** using a single launch command (`custom_launchfile`).

## Overview

This repository bundles the core TurtleBot3 ROS 2 packages alongside a custom launch package (`custom_launchfile`) that brings up:
- **Gazebo Simulation** (`turtlebot3_world.launch.py`) with the `burger` robot model configured automatically
- **ROS 2 Navigation2 (Nav2)** (`navigation2.launch.py`) pre-configured with simulation time (`use_sim_time:=true`) and a pre-generated occupancy grid map (`maps/map.yaml` and `maps/map.pgm`)
- **RViz2** pre-configured for 2D pose estimation and autonomous goal navigation

## Repository Structure

| Directory / Package | Description |
| :--- | :--- |
| `custom_launchfile/` | Custom ROS 2 Python package containing `nav2_bringup.launch.py` and the pre-built map (`maps/map.yaml`, `maps/map.pgm`) |
| `turtlebot3/` | Core TurtleBot3 ROS 2 metapackage (`turtlebot3_bringup`, `turtlebot3_navigation2`, `turtlebot3_cartographer`, `turtlebot3_description`, `turtlebot3_teleop`, `turtlebot3_node`) |
| `turtlebot3_simulations/` | Gazebo simulation worlds, models, and fake node packages (`turtlebot3_gazebo`, `turtlebot3_fake_node`) |
| `turtlebot3_msgs/` | Custom ROS 2 message, service, and action definitions for TurtleBot3 |
| `DynamixelSDK/` | ROBOTIS Dynamixel SDK libraries required by TurtleBot3 packages |

## Prerequisites

Ensure you have the following installed on Ubuntu with **ROS 2** (such as Humble or Foxy):

1. **ROS 2 Base / Desktop** sourced in your environment (`/opt/ros/$ROS_DISTRO/setup.bash`)
2. **Colcon & Rosdep** build tools:
   ```bash
   sudo apt update
   sudo apt install -y python3-colcon-common-extensions python3-rosdep git
   ```
3. **Gazebo, Nav2, and Cartographer** system packages:
   ```bash
   sudo apt install -y \
     ros-$ROS_DISTRO-gazebo-ros-pkgs \
     ros-$ROS_DISTRO-navigation2 \
     ros-$ROS_DISTRO-nav2-bringup \
     ros-$ROS_DISTRO-cartographer \
     ros-$ROS_DISTRO-cartographer-ros
   ```

## Installation & Build Instructions

Because the repository contains ROS 2 packages at its root, clone it inside the `src` directory of a ROS 2 workspace:

```bash
# 1. Create a ROS 2 workspace and navigate to src/
mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src

# 2. Clone this repository
git clone https://github.com/shivam-sensei/turtlebot3.git

# 3. Install any missing ROS dependencies via rosdep
cd ~/turtlebot3_ws
sudo rosdep init 2>/dev/null || true
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# 4. Build the workspace
colcon build --symlink-install

# 5. Source the workspace overlay
source ~/turtlebot3_ws/install/setup.bash
```

To avoid re-sourcing in every new terminal, optionally add the workspace and Gazebo model path to your `~/.bashrc`:

```bash
echo "source ~/turtlebot3_ws/install/setup.bash" >> ~/.bashrc
echo "export GAZEBO_MODEL_PATH=\$GAZEBO_MODEL_PATH:\$(ros2 pkg prefix turtlebot3_gazebo)/share/turtlebot3_gazebo/models" >> ~/.bashrc
source ~/.bashrc
```

## Launching the Simulation & Navigation Stack

### 1. Unified Single-Command Launch (Gazebo + Nav2 + RViz2)

The `custom_launchfile` package starts the Gazebo TurtleBot3 world, loads the custom map (`custom_launchfile/maps/map.yaml`), sets `TURTLEBOT3_MODEL=burger`, and launches Nav2 + RViz2 in a single command:

```bash
source ~/turtlebot3_ws/install/setup.bash
ros2 launch custom_launchfile nav2_bringup.launch.py
```

### 2. Navigating in RViz2

Once Gazebo and RViz2 open:
1. Click **2D Pose Estimate** in the top toolbar of RViz2.
2. Click and drag on the map matching the robot's initial position and orientation in the Gazebo world (so the laser scan aligns with the map walls).
3. Click **Nav2 Goal** (or **2D Goal Pose**) in the top toolbar and click/drag on any free space in the map to command the TurtleBot3 to autonomously navigate there.

### 3. Passing a Custom Map (Optional)

You can override the default map file at runtime using the `map` launch argument:

```bash
ros2 launch custom_launchfile nav2_bringup.launch.py map:=/absolute/path/to/your_map.yaml
```

## Optional Workflows

### Keyboard Teleoperation

To manually drive the robot in a separate terminal:

```bash
source ~/turtlebot3_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 run turtlebot3_teleop teleop_keyboard
```

### Creating a New Map with SLAM (Cartographer)

If you want to generate a fresh map of the Gazebo environment:

```bash
# Terminal 1: Launch Gazebo world
source ~/turtlebot3_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# Terminal 2: Launch Cartographer SLAM
source ~/turtlebot3_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True

# Terminal 3: Save the map once exploration is complete
ros2 run nav2_map_server map_saver_cli -f ~/turtlebot3_ws/src/turtlebot3/custom_launchfile/maps/my_new_map
```
