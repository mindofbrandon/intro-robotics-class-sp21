#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from mystery_package.msg import UnitsLabelled
rospy.set_param("units", "meters")

class Converter:
    def __init__(self):
        rospy.Subscriber("/mystery/output2", UnitsLabelled, self.callback)  # subscribe to output2 topic from mystery node
        self.pub = rospy.Publisher("converted_total", UnitsLabelled, queue_size=10)  # node is publishing topic to converted_total
        self.pub_msg = UnitsLabelled()
        self.pub_msg.units = "feet"

    def callback(self, msg):
        if rospy.has_param("units"):
            self.units = rospy.get_param("units")
        if self.units == "meters":
            self.units = rospy.get_param("units")
            self.pub_msg.units = "meters"  # convert meters to feet and store value
            self.pub.publish(msg.value, self.units)  # publish value to rostopic echo meterstofeet
            rospy.loginfo("%s %s", msg.value, self.pub_msg.units)  # output the conversion

        elif self.units == "feet":
            self.units = rospy.get_param("units")
            self.pub_msg.units = "feet"  # convert meters to feet and store value
            self.pub.publish(msg.value, self.units)  # publish value to rostopic echo meterstofeet
            rospy.loginfo("%s %s", msg.value, self.pub_msg.units)  # output the conversion

        elif self.units == "smoots":
            self.units = rospy.get_param("units")
            self.pub_msg.units = "smoots"  # convert meters to feet and store value
            self.pub.publish(msg.value, self.pub_msg.units)  # publish value to rostopic echo meterstofeet
            rospy.loginfo("%s %s", msg.value, self.units)  # output the conversion



if __name__ == '__main__':
    rospy.init_node('converter')
    Converter()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()