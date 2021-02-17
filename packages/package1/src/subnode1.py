#!/usr/bin/env python3
# adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy
from std_msgs.msg import Float32
from mystery_package.msg import UnitsLabelled


class Listener:
    def __init__(self):
        rospy.Subscriber("/output1", Float32, self.cb_out1)  # subscribe to each topic mys_node publishes?
        rospy.Subscriber("/output2", UnitsLabelled, self.cb_out2)  # subscribe to each topic mys_node publishes?

    def cb_out1(self, msg):
        rospy.loginfo("Output 1 published %s", msg.data)  # this never reaches in roscore

    def cb_out2(self, msg):
        rospy.loginfo("Output 2 published %s %s", msg.value, msg.units)  # this never reaches in roscore

if __name__ == '__main__':
    rospy.init_node('subnode1', anonymous=False)  # should this be "mystery_node"?
    Listener()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
