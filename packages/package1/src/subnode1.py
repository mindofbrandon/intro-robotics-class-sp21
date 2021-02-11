#!/usr/bin/env python3
# adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy
from std_msgs.msg import Float32
from mystery_package.msg import UnitsLabelled


class Listener:
    def __init__(self):
        rospy.Subscriber("/output1", Float32, self.callback)             # subscribe to each topic mys_node publishes
        rospy.Subscriber("/output2", UnitsLabelled, self.callback)       # subscribe to each topic mys_node publishes

    def callback(self, msg):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", msg.data)



if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)                         # should this be "mystery_node"?
    Listener()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()