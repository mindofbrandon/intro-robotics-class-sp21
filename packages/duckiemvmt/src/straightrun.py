#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped, FSMState, BoolStamped  # contains Header header, float32 v, float32 omega
#
# float32 v controls forward velocity
# float32 omega controls angular velocity


class StraightRun:
    def __init__(self):
        self.pub = rospy.Publisher("car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)  # publish to car_cmd to imitate lane following
        rospy.Subscriber("fsm_node/mode", FSMState, self.cb_state)  # subscribe
        self.pub_state = FSMState()
        rospy.loginfo("received %s", self.pub_state)
        # add a subscriber to listen to fsm state
        # need a flag to figure out fsm state

        # NORMAL_JOYSTICK_CONTROL
        # LANE_FOLLOWING

    def cb_state(self, state):
        rospy.loginfo("received %s", self.pub_state)  # output the conversion


if __name__ == '__main__':
    rospy.init_node('straightrun')
    StraightRun()  # needs to be used for movefwd and stop functions
    # i = 0
    # rate = rospy.Rate(1)  # 1Hz, loops once per second

    # while i < 10:
    #     s.movefwd(1)
    #     i += 1
    # s.stop()
    # cb_state(self)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
