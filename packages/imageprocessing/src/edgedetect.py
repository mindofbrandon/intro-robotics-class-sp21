#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
# uint32 height
# uint32 width
# string encoding
# uint8 is_bigendian
# uint32 step
# uint8[] data
from cv_bridge import CvBridge
import numpy as np
import math  # for pi


class EdgeDetect:
    def __init__(self):
        rospy.Subscriber("image_cropped", Image, self.cb_cropped)  # subscribe
        rospy.Subscriber("image_white", Image, self.cb_white)  # subscribe
        rospy.Subscriber("image_yellow", Image, self.cb_yellow)  # subscribe

        self.pub_canny_edge = rospy.Publisher("canny_edge", Image, queue_size=10)  # publish to imagee
        self.pub_lines_white = rospy.Publisher("image_lines_white", Image, queue_size=10)  # publish to image_lines_white
        self.pub_lines_yellow = rospy.Publisher("image_lines_yellow", Image, queue_size=10)  # publish to image_lines_yellow
        self.bridge = CvBridge()  # used to convert b/t ros and cvimages
        self.cv_cropped = 0
        self.canny = 0
        # self.cv_canny_mono = 0
        # roslaunch image_processing_hw image_pub.launch index:=2
        # change index number if you wanna try with another image

    def output_lines(self, original_image, lines):
        output = np.copy(original_image)
        if lines is not None:
            for i in range(len(lines)):
                l = lines[i][0]
                cv2.line(output, (l[0], l[1]), (l[2], l[3]), (255, 0, 0), 2, cv2.LINE_AA)
                cv2.circle(output, (l[0], l[1]), 2, (0, 255, 0))
                cv2.circle(output, (l[2], l[3]), 2, (0, 0, 255))
        return output

    def cb_cropped(self, msg_cropped):
        # convert to a ros image using the bridge
        self.cv_cropped = self.bridge.imgmsg_to_cv2(msg_cropped, "bgr8")

        # perform canny transform
        self.canny = cv2.Canny(self.cv_cropped, 120, 160)
        cv_canny_mono = self.bridge.cv2_to_imgmsg(self.canny, "mono8")

        # publish edited image
        self.pub_canny_edge.publish(cv_canny_mono)



    def cb_white(self, msg_white):
        cv_white = self.bridge.imgmsg_to_cv2(msg_white, "mono8")

        # mask both images
        # OR both images to get both grayscales together
        # cropped_white_mask = cv2.bitwise_or(cv_white, cv_white)

        # erode and shrink to get cleaner image
        # kernel_white = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # image_erode = cv2.erode(cv_cropped, kernel_white)
        # what should be done here?
        # this needs to be changed to get more solid lines

        # AND both images
        cropped_white_out = cv2.bitwise_and(self.canny, self.canny, mask=cv_white)


        # longer lines segments are showcased by less (-) and (+) icons
        # perform hough transform
        hough_white = cv2.HoughLinesP(cropped_white_out, 1, math.pi/180, 8, minLineLength=5, maxLineGap=3)
        # after pi/180, arg is:
        # threshold


        # need to get color back from hough transform
        edited_hough_white = self.output_lines(self.cv_cropped, hough_white)

        # convert new image back to ros in order to publish
        # ros_white_final = self.bridge.cv2_to_imgmsg(cropped_white_out, "mono8")
        ros_white_final = self.bridge.cv2_to_imgmsg(edited_hough_white, "bgr8")


        # publish edited image
        self.pub_lines_white.publish(ros_white_final)

    def cb_yellow(self, msg_yellow):

        cv_yellow = self.bridge.imgmsg_to_cv2(msg_yellow, "mono8")

        # mask both images
        # OR both images to get both grayscales together
        # cropped_yellow_mask = cv2.bitwise_or(cv_yellow, cv_yellow)

        # AND both images
        cropped_yellow_out = cv2.bitwise_and(self.canny, self.canny, mask=cv_yellow)

        # perform hough transform
        hough_yellow = cv2.HoughLinesP(cropped_yellow_out, 1, math.pi/180, 8, minLineLength=5, maxLineGap=3)

        # need to get color back from hough transform
        edited_hough_yellow = self.output_lines(self.cv_cropped, hough_yellow)

        # convert new image back to ros in order to publish
        # ros_yellow_final = self.bridge.cv2_to_imgmsg(cropped_yellow_out, "mono8")
        ros_yellow_final = self.bridge.cv2_to_imgmsg(edited_hough_yellow, "bgr8")

        # publish edited image
        self.pub_lines_yellow.publish(ros_yellow_final)


if __name__ == '__main__':
    rospy.init_node('edgedetect')
    EdgeDetect()  # calls class
    rospy.spin()
