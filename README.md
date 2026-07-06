# TortoiseBot Waypoints

This package implements a ROS1 action server that navigates the TortoiseBot to a specified waypoint in the Gazebo simulation. It aims to practice ROS1 testing for the action server.

> **Note:** This package is intended to be run using the **CP23 ROSject** on The Construct.

## Running the Test

### Terminal 1 – Launch Gazebo

```bash
source /opt/ros/noetic/setup.bash
source ~/simulation_ws/devel/setup.bash

roslaunch tortoisebot_gazebo tortoisebot_playground.launch
```

> If Gazebo freezes or fails to launch properly, terminate it (`kill -9 <gazebo_pid>`) and relaunch it.

### Terminal 2 – Launch the Action Server

```bash
source /opt/ros/noetic/setup.bash

cd ~/simulation_ws
catkin_make
source devel/setup.bash

rosrun tortoisebot_waypoints tortoisebot_action_server.py
```

Keep both terminals running while executing the tests.

---

## Passing Condition

Open:

```text
test/waypoints_test.test
```

Set the waypoint goal to:

```xml
<param name="goal_x" value="0.4"/>
<param name="goal_y" value="0.4"/>
```

Run:

```bash
source /opt/ros/noetic/setup.bash
cd ~/simulation_ws
catkin_make
source devel/setup.bash

rostest tortoisebot_waypoints waypoints_test.test --reuse-master
```

**Expected result:** All tests pass.

---

## Failing Condition

Edit the same file:

```text
test/waypoints_test.test
```

Change the waypoint goal to:

```xml
<param name="goal_x" value="2.0"/>
<param name="goal_y" value="2.0"/>
```

Run the same command again:

```bash
source /opt/ros/noetic/setup.bash
cd ~/simulation_ws
catkin_make
source devel/setup.bash

rostest tortoisebot_waypoints waypoints_test.test --reuse-master
```

**Expected result:** all tests fail.