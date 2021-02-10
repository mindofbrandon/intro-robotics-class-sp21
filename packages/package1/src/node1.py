#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

        # Program to display the Fibonacci sequence up to n-th term
        # first two terms
        n1, n2 = 0, 1
        count = 0

        pub.publish(n1)
        rate.sleep()

        nth = n1 + n2
        # update values
        n1 = n2
        n2 = nth

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
