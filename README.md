# Digital-Twin-For-KR16-Kuka-arm


This repository contains the URDF model and ROS 2 Humble integration for a simulated KUKA robotic arm. It includes control configuration using `ros2_control`, transmission setup, MQTT communication, and Gazebo simulation support.

## Features

- ✅ KUKA arm URDF with xacro support  
- ✅ Integrated with `ros2_control` for hardware interface simulation  
- ✅ Transmission and joint interfaces configured  
- ✅ Gazebo simulation ready  
- ✅ MQTT integration for external IoT communication  
- ✅ Modular workspace setup (`antonious_boshra_kuka_arm`)  
- ✅ UnityMCP server path support (if applicable)

## Getting Started

### Prerequisites

- ROS 2 Humble installed on Linux  
- Gazebo (compatible with ROS 2)  
- Colcon build system  
- UnityMCP (optional) if using Unity integration  
- MQTT broker (e.g., Mosquitto) for message-based IoT communication 
