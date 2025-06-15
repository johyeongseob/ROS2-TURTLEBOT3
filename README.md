# ROS2 & Ubuntu Development Environment Setup and Practice

Dongguk University | Department of Mechanical, Robotics, and Energy Engineering  
**Course**: 자율로봇실습 (MEC4092-01), Spring 2023
**Instructor**: Prof. Soo-Cheol Lim

This repository contains ROS2-based practical exercises for autonomous robotics using [**TurtleBot3**](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/).

---

## 🧱 Environment: ROS2 + TurtleBot3

- **ROS2 Version**: Humble
- **Robot Platform**: TurtleBot3

### What is ROS

- [ROS is an open-source, meta-operating system for your robot.](https://wiki.ros.org/)


## 🛠️ ROS2 Setup Guide

### ✅ ROS2 Humble Installation
📄 [Official Installation Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

### ✅ Install Build Tool: Colcon

```bash
sudo apt install python3-colcon-common-extensions
```

✅ Create ROS2 Workspace

```bash
cd ~
mkdir -p ros2_ws/src
cd ros2_ws
colcon build
```

✅ Update .bashrc

```bash
gedit ~/.bashrc
# Add the following at the end:
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
```

🐍 Python Node Example

📁 Node Setup

```bash
cd ~/ros2_ws/src/my_py_pkg/my_py_pkg
touch my_first_node.py
```

🔧 setup.py

```bash
entry_points={
    'console_scripts': [
        'py_node = my_py_pkg.my_first_node:main',
    ],
}
```

🚀 Run Python Node

🔹 Method 1

```bash
cd ~/ros2_ws
colcon build --packages-select my_py_pkg
source ~/.bashrc
cd install/my_py_pkg/lib/my_py_pkg
./py_node
```

🔹 Method 2

```bash
cd ~/ros2_ws
colcon build --packages-select my_py_pkg
# Open new terminal
source ~/.bashrc
ros2 run my_py_pkg py_node
```

📦 Create Python Package

```bash
cd ~/ros2_ws/src
ros2 pkg create [package_name] --build-type ament_python --dependencies rclpy
```

🧪 Build Your Package

✅ Method 1

```bash
cd ~/ros2_ws
colcon build --packages-select [package]
source install/local_setup.bash
```

✅ Method 2 (recommended for development)

```bash
cd ~/ros2_ws
colcon build --packages-select [package] --symlink-install
```

🧰 Useful ROS2 Commands


| Command                       | Description                             |
| ----------------------------- | --------------------------------------- |
| `ros2 node list`              | List active nodes                       |
| `ros2 node info /node_name`   | Get info of a specific node             |
| `ros2 topic list`             | List active topics                      |
| `ros2 topic echo /topic_name` | Print messages from a topic             |
| `rqt`                         | Launch ROS2 GUI tool (rqt\_graph, etc.) |


🛰️ Publisher & Subscriber Example

📝 Publisher: robot_news_station.py

```bash
cd ~/ros2_ws/src/my_py_pkg/my_py_pkg
touch robot_news_station.py
chmod +x robot_news_station.py
# Modify code, setup.py, and package.xml
cd ~/ros2_ws
colcon build --packages-select my_py_pkg --symlink-install
source ~/.bashrc
```

📝 Subscriber: smartphone.py

```bash
cd ~/ros2_ws/src/my_py_pkg/my_py_pkg
touch smartphone.py
chmod +x smartphone.py
# Same build and setup steps as above
```


📎 Notes

- Ensure both publisher and subscriber use the same message type.
- Don't run multiple nodes with the same name simultaneously.
- Always source your workspace after building:

```bash
source ~/.bashrc
```


