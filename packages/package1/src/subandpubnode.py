#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from mystery_package.msg import UnitsLabelled


class SubAndPub:
    def __init__(self):
        rospy.Subscriber("/output2", UnitsLabelled, self.callback)  # subscribe to output2 topic from mystery node
        self.pub = rospy.Publisher("meterstofeet", UnitsLabelled, queue_size=10)  # node is publishing to
        self.pub_msg = UnitsLabelled()
        self.pub_msg.units = "feet"
        # meterstofeet topic

        # self.pub_msg = UnitsLabelled()  # output value so you can see it when doing rostopic echo
        # self.pub_msg.units = "feet"

    def callback(self, msg):
        datatofeet = msg.value * 3.2808  # convert meters to feet and store value
        rospy.loginfo("%s converted: %s feet", msg.value, datatofeet)  # output the conversion
        self.pub.publish(datatofeet, self.pub_msg.units)  # publish value to rostopic echo meterstofeet
        # self.pub_msg.units.publish(self.pub_msg.units)  # publish units to rostopic echo meterstofeet


if __name__ == '__main__':
    rospy.init_node('subandpubnode')
    SubAndPub()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
