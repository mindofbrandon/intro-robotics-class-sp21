#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
from picamera import PiCamera
import numpy as np

class LaneDetector:
    def __init__(self):
        rospy.Subscriber("camera_node/image/compressed", CompressedImage, self.cb, queue_size=1, buff_size=2**24)
        self.pub_cropped = rospy.Publisher("image_cropped", Image, queue_size=10)  # publish to image_cropped
        self.pub_white = rospy.Publisher("image_white", Image, queue_size=10)  # publish to image_white
        self.pub_yellow = rospy.Publisher("image_yellow", Image, queue_size=10)  # publish to image_yellow
        self.pub_masked = rospy.Publisher("image_mask", Image, queue_size=10)  # publish the complete masked image to image_mask
        self.bridge = CvBridge()  # used to convert b/t ros and cvimages

        # roslaunch image_processing_hw image_pub.launch index:=2
        # change index number if you wanna try with another image

    def cb(self, msg):
        # convert to a ros image using the bridge
        cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

        # ------ CROPPED IMAGE ------

        # ground projection node asks for 120x160 pixels (LxW), and remove the top 4 pixels from the image
        image_size = (160, 120)
        offset = 40
        new_image = cv2.resize(cv_image, image_size, interpolation=cv2.INTER_NEAREST)
        cv_cropped = new_image[offset:, :]


        # convert new image back to ros in order to publish
        ros_cropped_final = self.bridge.cv2_to_imgmsg(cv_cropped, "bgr8")

        # publish edited image
        self.pub_cropped.publish(ros_cropped_final)

        # ------ WHITE AND YELLOW MASKS AND PUBLISHING ------
        # convert cropped image to HSV (hue, saturation, value)
        hsv_image = cv2.cvtColor(cv_cropped, cv2.COLOR_BGR2HSV)

        # extract relevant colors (white and yellow for duckietown lanes)
        # this produces a binary image (if white, there was the color we needed; if black, color was not there)
        # cv2.inRange(cv_cropped, lower_bound, upper_bound)
        # bounds notated as (hue, saturation, value)
        # hue is number of color that remains
        # saturation is number of distance from white
        # value is number of distance from black
        # hue range = 0-179
        # sat and val range = 0-255

        # ------ WHITE MASK AND PUBLISHING ------
        cv_white = cv2.inRange(hsv_image, (0, 0, 100), (160, 30, 255))

        # erode and shrink to get cleaner image
        kernel_white = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        image_erode_white = cv2.erode(cv_white, kernel_white)

        # dilate and shrink to get cleaner image
        kernel_white = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        image_dilate_white = cv2.dilate(image_erode_white, kernel_white)
        #

        # mask both images
        # OR both images to get both grayscales together
        # mask_white = cv2.bitwise_or(image_erode_white, image_erode_white)


        # AND both images to get color back
        output_white = cv2.bitwise_and(cv_cropped, cv_cropped, mask=image_dilate_white)

        # convert new image back to ros in order to publish
        ros_white_final = self.bridge.cv2_to_imgmsg(output_white, "bgr8")

        # publish edited image
        self.pub_white.publish(ros_white_final)

        # ------ YELLOW MASK AND PUBLISHING ------
        cv_yellow = cv2.inRange(hsv_image, (27, 50, 150), (30, 255, 255))

        # dilate and shrink to get cleaner image
        kernel_yellow = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        image_dilate_yellow = cv2.dilate(cv_yellow, kernel_yellow)
        #

        # mask both images
        # OR both images to get both grayscales together
        # mask_yellow = cv2.bitwise_or(cv_yellow, cv_yellow)



        # AND both images to get color back
        output_yellow = cv2.bitwise_and(cv_cropped, cv_cropped, mask=image_dilate_yellow)
        # i try to change to mask=image_dilate but it does not work

        # convert new image back to ros in order to publish
        ros_yellow_final = self.bridge.cv2_to_imgmsg(output_yellow, "bgr8")
        # compressed_imgmsg_to_cv2

        # publish edited image
        self.pub_yellow.publish(ros_yellow_final)

        # ------ BOTH TOGETHER AND PUBLISHING ------
        # This part was not required, but I kept it so that I could get a better understanding

        # mask both images
        # OR both images to get both grayscales together
        mask = cv2.bitwise_or(output_white, output_yellow)

        # AND both images to get color back
        # output = cv2.bitwise_and(cv_cropped, cv_cropped, mask=mask)

        # convert new image back to ros in order to publish
        ros_edited = self.bridge.cv2_to_imgmsg(mask, "bgr8")

        # publish edited image
        self.pub_masked.publish(ros_edited)


if __name__ == '__main__':
    rospy.init_node('lanedetector')
    LaneDetector()  # calls class
    rospy.spin()
