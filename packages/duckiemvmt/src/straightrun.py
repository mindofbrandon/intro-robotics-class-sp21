#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped  # contains Header header, float32 v, float32 omega
#
# float32 v controls forward velocity
# float32 omega controls angular velocity


class StraightRun:
    def __init__(self):
        self.pub = rospy.Publisher("/car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)  # publish to car_cmd to imitate lane following

    def movefwd(self, fwdvelocity):
        movement = Twist2DStamped()
        movement.v = fwdvelocity
        self.pub.publish(movement)

    def stop(self):
        movement = Twist2DStamped()
        movement.v = 0


if __name__ == '__main__':
    rospy.init_node('straightrun')
    i = 0
    rate = rospy.Rate(1)  # 1Hz, loops once per second

    while i < 10:
        movefwd(1)
        i += 1
    stop()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
