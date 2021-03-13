#!/usr/bin/env python3

import rospy
import numpy  # for matrices
import math  # cos and sin
from std_msgs.msg import Float32
from duckietown_msgs.msg import Vector2D


class CoordTF:
    def __init__(self):
        rospy.Subscriber("inputcoord", Vector2D, self.callback)
        # to input val do this in ros: rostopic pub /homework5/inputcoord duckietown_msgs/Vector2D 1 3
        # to input negative vals: rostopic pub /homework5/inputcoord duckietown_msgs/Vector2D 7 -- -6
        # to input to echo once a second: rostopic pub /homework5/inputcoord duckietown_msgs/Vector2D 3 2 -r 1
        self.robot = rospy.Publisher("robotcoord", Vector2D, queue_size=10)
        self.world = rospy.Publisher("worldcoord", Vector2D, queue_size=10)

    def callback(self, values):
        # initialize matrix 1
        rts = numpy.matrix([[-1, 0, -1], [0, -1, 0], [0, 0, 1]])
        # | -1  0 -1 |
        # |  0 -1  0 |
        # |  0  0  1 |

        # initialize matrix 2
        # vals arent working if the math is done in the matrix
        val1 = -math.sqrt(2) / 2
        val2 = -math.sqrt(2) / 2
        val3 = math.sqrt(2) / 2
        val4 = -math.sqrt(2) / 2

        wtr = numpy.matrix([[val1, val2, 10], [val3, val4, 5], [0, 0, 1]])
        # | -.707  -.707  10 |
        # |  .707  -.707   5 |
        # |     0      0   1 |

        # subscribe to input and do calculations with matrices
        x_coord = values.x  # save x coord
        y_coord = values.y  # save y coord
        rpx = numpy.matrix([[x_coord], [y_coord], [1]])
        # for example obstacle @ 3,2
        # |3|
        # |2|
        # |1| -> is the quaternion?
        robotcoord = rts * rpx  # answer in robot coords
        self.robot.publish(robotcoord[0, 0], robotcoord[1, 0])  # publish robot coord

        # obstacles in world coord
        worldcoord = wtr * robotcoord # answer in world coords
        self.world.publish(worldcoord[0, 0], worldcoord[1, 0])






if __name__ == '__main__':
    rospy.init_node('coordtransform')
    CoordTF()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
