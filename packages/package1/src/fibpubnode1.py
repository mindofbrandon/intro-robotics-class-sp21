#!/usr/bin/env python3
# Adapted from https://www.programiz.com/python-programming/examples/fibonacci-sequence

import rospy
from std_msgs.msg import String

n1 = 0
n2 = 1


def fib():
    return n1


def talker():
    pub = rospy.Publisher("/input", String, queue_size=10)  # node is pub to "chatter" topic; should this be "input"?
    rospy.init_node('talker', anonymous=True)  # tells rospy the name of node is "talker"
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
