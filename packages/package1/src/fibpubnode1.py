#!/usr/bin/env python3
# Adapted from https://www.programiz.com/python-programming/examples/fibonacci-sequence

import rospy
from std_msgs.msg import String

n1 = 0
n2 = 1


def fib():

    return n1


def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)  # 1Hz
    while not rospy.is_shutdown():
        global n1
        global n2
        rospy.loginfo(str(fib()))
        pub.publish(str(fib()))
        nth = n1 + n2
        n1 = n2
        n2 = nth
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
