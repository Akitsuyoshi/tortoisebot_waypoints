#! /usr/bin/env python

import unittest
import rospy
import math
import actionlib

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point
from tf.transformations import euler_from_quaternion
from tortoisebot_waypoints.msg import (
    WaypointActionAction,
    WaypointActionGoal
)

class TestWaypointAction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Runs only once, not every before each test
        cls.client = actionlib.SimpleActionClient("tortoisebot_as", WaypointActionAction)
        cls.client.wait_for_server(rospy.Duration(10))
        rospy.sleep(1.0)

        target_x = rospy.get_param("~target_x", 0.4)
        target_y = rospy.get_param("~target_y", 0.4)
        
        # Set and send the goal once
        cls.goal_msg = WaypointActionGoal()
        cls.goal_msg.position = Point(target_x, target_y, 0.0)
        cls.client.send_goal_and_wait(cls.goal_msg, rospy.Duration(20))

        cls.final_odom = rospy.wait_for_message("/odom", Odometry, timeout=10)
         
    def euler_to_quaternion(self, msg):
        orientations = [msg.x, msg.y, msg.z, msg.w]
        (_, _, yaw) = euler_from_quaternion(orientations)
        return yaw
    
    def test_position_error(self):
        final_x = self.final_odom.pose.pose.position.x
        final_y = self.final_odom.pose.pose.position.y

        dx = abs(self.goal_msg.position.x - final_x)
        dy = abs(self.goal_msg.position.y - final_y)

        print(f"Position x error: {dx}")
        print(f"Position y error: {dy}")

        self.assertLess(dx, 0.05, "Position x error is too big")
        self.assertLess(dy, 0.05, "Position y error is too big")
    
    def test_yaw_error(self):
        final_yaw = self.euler_to_quaternion(self.final_odom.pose.pose.orientation)
        expected_yaw = math.atan2(self.goal_msg.position.y, self.goal_msg.position.x)

        # Normalize yaw error
        yaw_err = final_yaw - expected_yaw
        yaw_err = abs(math.atan2(math.sin(yaw_err), math.cos(yaw_err)))
        print(f"Orientation yaw error: {yaw_err}")

        self.assertLess(yaw_err, 0.15, "Orientation yaw error is too big")


if __name__ == "__main__":
    import rostest
    rospy.init_node("test_waypoint_action")
    rostest.rosrun("tortoisebot_waypoints", "test_waypoint_action", TestWaypointAction)