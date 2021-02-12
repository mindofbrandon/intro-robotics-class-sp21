#!/usr/bin/env python3
# Adapted from https://www.programiz.com/python-programming/examples/fibonacci-sequence

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32

n1 = 0
n2 = 1


def fib():
    return n1


def talker():
    pub = rospy.Publisher("/input", Float32, queue_size=10)  # node is publishing to input topic?
    rospy.init_node('fibpubnode1', anonymous=True)  # tells rospy the name of node is "fibpubnode1"
    rate = rospy.Rate(1)  # 1Hz, loops once per second
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
