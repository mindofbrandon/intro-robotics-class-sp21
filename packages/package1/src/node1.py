#!/usr/bin/env python3
# Adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy
from std_msgs.msg import String

n1, n2 = 0, 1


class Talker:
    def __init__(self):
        self.pub = rospy.Publisher('chatter', String, queue_size=10)


if __name__ == '__main__':
    try:
        rospy.init_node('talker', anonymous=True)
        t = Talker()
        rate = rospy.Rate(.0001)  # 1hz
        while not rospy.is_shutdown():
            rospy.loginfo(n1)
            self.pub.publish(n1)
            nth = n1 + n2
            # update values
            n1 = n2
            n2 = nth

            rate.sleep()
    except rospy.ROSInterruptException:
        pass
