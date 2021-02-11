#!/usr/bin/env python3
# Adapted from https://www.programiz.com/python-programming/examples/fibonacci-sequence

import rospy
from std_msgs.msg import String

n1, n2 = 0, 1               # initial terms for Fibonacci sequence


class Talker:
    def __init__(self): # run as soon as an object is created

        # declares that node is publishing to topic (topic = chatter)
        self.pub = rospy.Publisher('chatter', String, queue_size=10)


if __name__ == '__main__':
    try:
        rospy.init_node('talker', anonymous=True) # tells the name of the node (node = talker)
        # t = Talker()
        rate = rospy.Rate(1)  # 1hz
        while not rospy.is_shutdown():
            # rospy.loginfo(n1)
            # self.pub.publish(n1)
            # print(n1)
            nth = n1 + n2
            # update values
            n1 = n2
            n2 = nth

            rate.sleep()
    except rospy.ROSInterruptException:
        pass

#######################################################################################################################
# !/usr/bin/env python3
# Adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy
from std_msgs.msg import String


class Talker:
    def __init__(self):
        self.pub = rospy.Publisher('chatter', String, queue_size=10)

    def talk(self):
        if n <= 1:
            return n
        else:
            return recur_fibo(n - 1) + recur_fibo(n - 2)

        rospy.loginfo(hello_str)
        self.pub.publish(hello_str)


if __name__ == '__main__':
    try:
        rospy.init_node('talker', anonymous=True)
        t = Talker()
        rate = rospy.Rate(1)  # 1hz
        while not rospy.is_shutdown():
            t.talk()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass