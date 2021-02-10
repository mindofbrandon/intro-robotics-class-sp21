#!/usr/bin/env python3
# Adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy
from std_msgs.msg import String


class Talker:
    def __init__(self):
        self.pub = rospy.Publisher('chatter', String, queue_size=10)

    def talk(self):
        n1, n2 = 0, 1
        while True:

            rospy.loginfo(n1)
            self.pub.publish(n1)
            nth = n1 + n2
            # update values
            n1 = n2
            n2 = nth


if __name__ == '__main__':
    try:
        rospy.init_node('talker', anonymous=True)
        t = Talker()
        rate = rospy.Rate(.01)  # 1hz
        while not rospy.is_shutdown():
            t.talk()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass