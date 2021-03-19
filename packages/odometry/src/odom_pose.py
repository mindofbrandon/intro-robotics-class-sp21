#!/usr/bin/env python3

import rospy
import math
# from std_msgs.msg import Float32
from duckietown_msgs.msg import Pose2DStamped  #
from odometry_hw.msg import DistWheel  # needed for publisher
# float64 dist_wheel_left
# float64 dist_wheel_right

from odometry_hw.msg import Pose2D


# float64 x
# float64 y
# float64 theta

class OdomPose:
    def __init__(self):
        rospy.Subscriber("/dist_wheel", DistWheel, self.cb_dist)  # subscribe to get wheel movement
        self.odom = rospy.Publisher("/pose", Pose2D, queue_size=10)  # publish to /pose
        self.odom_positions = Pose2D()

    def cb_dist(self, msg):

        movement_left = msg.dist_wheel_left # how to get previous movement added to new movement?
        movement_right = msg.dist_wheel_right

        rospy.loginfo("movement at left wheel:%s movement at right wheel: %s", movement_left, movement_right)

        xpos_initial = 0
        ypos_initial = 0
        theta_initial = 0

        delta_s = (movement_left + movement_right) / 2  # arc length
        alpha = (movement_right - movement_left) / (2 * .1)  # Assume that the baseline (distance) between wheels (front or back) 2L=0.1m (so L=0.05m) and wheel distances are given are in meters.
        delta_theta = alpha
        # alpha is angle which equals delta_theta

        val_cos = math.cos(theta_initial + delta_theta / 2)
        val_sin = math.sin(theta_initial + delta_theta / 2)

        delta_x = delta_s * val_cos
        delta_y = delta_s * val_sin




        # xpos_new = xpos_initial + delta_x
        # ypos_new = ypos_initial + delta_y
        # theta_new = theta_initial + delta_theta

        xpos_initial = xpos_initial + delta_x
        ypos_initial = ypos_initial + delta_y
        theta_initial = theta_initial + delta_theta


        self.odom_positions.x = xpos_initial
        self.odom_positions.y = ypos_initial
        self.odom_positions.theta = theta_initial

        # rospy.loginfo("mvmt @ x: %s, mvmt @ y: %s, mvmt @ theta: %s", xpos_initial, ypos_initial, theta_initial)

        self.odom.publish(self.odom_positions)
        # calculate left right and theta assuming robot starts @ x, y, z = 0
        # publish the current pose to /pose


if __name__ == '__main__':
    rospy.init_node('odom_pose')
    OdomPose()  # needs to be used for movefwd and stop functions
    rospy.spin()
