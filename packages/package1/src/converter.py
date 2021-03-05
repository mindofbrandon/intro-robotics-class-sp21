#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from mystery_package.msg import UnitsLabelled
# rospy.set_param("meters", "meters")
# rospy.set_param("feet", "feet")
# rospy.set_param("smoots", "smoots")


class Converter:
    def __init__(self):
        rospy.Subscriber("/mystery/output2", UnitsLabelled, self.callback)  # subscribe to output2 topic from mystery node
        self.pub = rospy.Publisher("converted_total", UnitsLabelled, queue_size=10)  # node is publishing topic to converted_total
        self.pub_msg = UnitsLabelled()
        # self.pub_msg.units = "meters"

        # meterstofeet topic

        # self.pub_msg = UnitsLabelled()  # output value so you can see it when doing rostopic echo
        # self.pub_msg.units = "feet"

    def callback(self, msg):

        if rospy.has_param("meters"):
            self.mode = rospy.get_param("meters")
            rospy.set_param("meters", self.mode)
            self.pub_msg.units = "meters"  # maybe if i change this in all of them it'll work?
            datainmeters = msg.value
            rospy.loginfo("%s %s", datainmeters, self.mode)  # output the conversion
            self.pub.publish(datainmeters, self.mode)  # publish value to rostopic echo converted_total

        elif rospy.has_param("feet"):
            self.mode = rospy.get_param("feet")
            rospy.set_param("feet", self.mode)
            # self.pub_msg.units = "feet"
            datatofeet = msg.value * 3.2808  # convert meters to feet and store value
            rospy.loginfo("%s %s", datatofeet, self.mode)  # output the conversion
            self.pub.publish(datatofeet, self.mode)  # publish value to rostopic echo converted_total

        elif rospy.has_param("smoots"):
            self.mode = rospy.get_param("smoots")
            rospy.set_param("smoots", self.mode)
            # self.pub_msg.units = "smoots"
            datatosmoots = msg.value * .587613  # convert meters to smoots and store value
            rospy.loginfo("%s %s", datatosmoots, self.mode)  # output the conversion
            self.pub.publish(datatosmoots, self.mode)  # publish value to rostopic echo converted_total


if __name__ == '__main__':
    rospy.init_node('subandpubnode')
    Converter()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()