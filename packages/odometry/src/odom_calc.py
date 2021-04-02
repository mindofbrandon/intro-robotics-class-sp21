#!/usr/bin/env python3
# This is lab3 and done on physical robot
import rospy
import math
# from std_msgs.msg import Float32
from duckietown_msgs.msg import Pose2DStamped, WheelsCmdStamped  # needed for subscribers

# from WheelsCmdStamped:
# Header header
# float32 vel_left
# float32 vel_right

# from Pose2DStamped:
# float64 x
# float64 y
# float64 theta

# velocity in straight code is .5
# actual velocity is 0.582343339920044

class OdomCalc:
    def __init__(self):
        rospy.Subscriber("wheels_driver_node/wheels_cmd", WheelsCmdStamped, self.cb_wheels)  # subscribe to get wheel movement
        self.odom = rospy.Publisher("physicalpose", Pose2DStamped, queue_size=10)  # publish to /physicalpose
        self.odom_positions = Pose2DStamped()

    def cb_wheels(self, msg):

        global i
        global xpos_initial
        global ypos_initial
        global theta_initial
        # rospy.loginfo("val i = %s", i)

        while (i < 1):
            xpos_initial = 0
            ypos_initial = 0
            theta_initial = 0
            i += 1
        # round(xpos_initial, 1)
        # round(ypos_initial, 1)
        # rospy.loginfo("zero once only %f %f %f", xpos_initial, ypos_initial, theta_initial)
        movement_left = msg.vel_left
        movement_right = msg.vel_right

        # rospy.loginfo("movement at left wheel:%s movement at right wheel: %s", movement_left, movement_right)



        delta_s = (movement_left + movement_right) / 2  # arc length
        delta_theta = (movement_right - movement_left) / (2 * .05)  # Assume that the baseline (distance) between wheels (front or back) 2L=0.1m (so L=0.05m) and wheel distances are given are in meters.
        # delta_theta = alpha
        # alpha is angle which equals delta_theta

        val_cos = math.cos(theta_initial + (delta_theta / 2))
        val_sin = math.sin(theta_initial + (delta_theta / 2))

        delta_x = delta_s * val_cos
        delta_y = delta_s * val_sin






        xpos_initial = xpos_initial + delta_x
        ypos_initial = ypos_initial + delta_y
        theta_initial = theta_initial + delta_theta

        # xpos_new = xpos_initial +
        # ypos_new = ypos_initial
        # theta_new = theta_initial



        self.odom_positions.x = xpos_initial
        self.odom_positions.y = ypos_initial  # divide by 100 to get meters
        self.odom_positions.theta = theta_initial

        # rospy.loginfo("mvmt @ x: %f, mvmt @ y: %f, mvmt @ theta: %s", round(xpos_initial, 2), ypos_initial, theta_initial)

        self.odom.publish(self.odom_positions)
        # calculate left right and theta assuming robot starts @ x, y, z = 0
        # publish the current pose to /pose


if __name__ == '__main__':
    rospy.init_node('odom_calc')
    i = 0
    OdomCalc()  # calls class to run code
    rospy.spin()
