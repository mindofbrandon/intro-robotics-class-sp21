#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped, FSMState, BoolStamped  #
#

class OdomPose:
    def __init__(self):
        rospy.Subscriber("fsm_node/mode", FSMState, self.cb_state)  # subscribe
        self.carnode = rospy.Publisher("car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)  # publish to car_cmd to imitate lane following
        self.carnode_move = Twist2DStamped()

        # NORMAL_JOYSTICK_CONTROL
        # LANE_FOLLOWING

    def cb_state(self, state_val):
        state = state_val.state


if __name__ == '__main__':
    rospy.init_node('odom_pose')
    OdomPose()  # needs to be used for movefwd and stop functions
    rospy.spin()