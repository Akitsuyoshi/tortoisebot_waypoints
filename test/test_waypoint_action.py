#! /usr/bin/env python

import unittest
import rospy
import actionlib

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point

class TestWaypointAction(unittest.TestCase):
    def setUp(self):
        rospy.loginfo("Start to test tortoisebot_as action server")
    
    def test_odom_available(self):
        topic_n = "/odom"
        try:
            msg = rospy.wait_for_message(topic_n, Odometry, timeout=5)
        except rospy.ROSException:
            self.fail(f"{topic_n} topic was not published")
        
        self.assertIsNotNone(msg)
    

if __name__ == "__main__":
    import rostest
    rospy.init_node("test_waypoint_action")
    rostest.rosrun("tortoisebot_waypoints", "test_waypoint_action", TestWaypointAction)