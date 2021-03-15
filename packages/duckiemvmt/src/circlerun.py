#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from duckietown_msgs.msg import Twist2DStamped, FSMState, BoolStamped  # contains Header header, float32 v, float32 omega
#
# float32 v controls forward velocity
# float32 omega controls angular velocity


class CircleRun:
    def __init__(self):
        rospy.Subscriber("fsm_node/mode", FSMState, self.cb_state)  # subscribe
        self.carnode = rospy.Publisher("car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)  # publish to car_cmd to imitate lane following
        self.carnode_move = Twist2DStamped()

        # NORMAL_JOYSTICK_CONTROL
        # LANE_FOLLOWING

    def cb_state(self, state_val):
        state = state_val.state
        i = 0

        if state == "NORMAL_JOYSTICK_CONTROL":
            print("state is: %s", state)
            rospy.loginfo("state is: %s", state)
            # self.carnode.publish(self.carnode_move)
        elif state == "LANE_FOLLOWING":


            rate = rospy.Rate(1)  # 1Hz, loops once per second
            rospy.loginfo("counter before: %s", i)
            # rospy.loginfo("state is: %s", state)
            while i < 6:
                self.carnode_move.v = .5
                self.carnode_move.omega = .2
                self.carnode.publish(self.carnode_move)
                rospy.loginfo("counter in loop: %s", i)
                i += 1
                rate.sleep()

            self.carnode_move.v = 0
            self.carnode_move.omega = 0
            self.carnode.publish(self.carnode_move)
            rospy.loginfo("counter at end: %s", i)
            rospy.loginfo("stop moving")



if __name__ == '__main__':
    rospy.init_node('circlerun')
    j = 0
    CircleRun()  # needs to be used for movefwd and stop functions
    # i = 0
    # rate = rospy.Rate(1)  # 1Hz, loops once per second

    # while i < 10:
    #     s.movefwd(1)
    #     i += 1
    # s.stop()
    # cb_state(self)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()