#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from mystery_package.msg import UnitsLabelled

class Converter:
    def __init__(self):
        rospy.Subscriber("/mystery/output2", UnitsLabelled, self.callback)  # subscribe to output2 topic from mystery node
        self.pub = rospy.Publisher("converted_total", UnitsLabelled, queue_size=10)  # node is publishing topic to converted_total
        self.pub_msg = UnitsLabelled()
        # self.pub_msg.units = ""

    def callback(self, msg):
        if rospy.has_param("units"):  # make sure parameter exists in launch file
            self.pub_msg.units = rospy.get_param("units")  # set default units (meters) to pub_msg.units

        if self.pub_msg.units == "meters":
            datainmeters = msg.value
            self.pub.publish(datainmeters, self.pub_msg.units)  # publish value to rostopic echo converter

        elif self.pub_msg.units == "feet":
            datainfeet = msg.value * 3.2808
            self.pub.publish(datainfeet, self.pub_msg.units)  # publish value to rostopic echo converter

        elif self.pub_msg.units == "smoots":
            datainsmoots = msg.value * .7018
            self.pub.publish(datainsmoots, self.pub_msg.units)  # publish value to rostopic echo converter



if __name__ == '__main__':
    rospy.init_node('converter')
    Converter()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()