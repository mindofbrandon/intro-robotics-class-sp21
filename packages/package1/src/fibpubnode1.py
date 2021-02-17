#!/usr/bin/env python3
# Adapted from https://www.programiz.com/python-programming/examples/fibonacci-sequence

import rospy
from std_msgs.msg import String
from std_msgs.msg import Float32

def talker():
    pub = rospy.Publisher("/input", Float32, queue_size=10)  # node is publishing to input topic?
    rospy.init_node('fibpubnode1', anonymous=False)  # tells rospy the name of node is "fibpubnode1"
    # anon = false to remove long tag at end of node
    rate = rospy.Rate(1)  # 1Hz, loops once per second
    n1 = 0
    n2 = 1
    while not rospy.is_shutdown():
        rospy.loginfo(n1)
        pub.publish(n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
