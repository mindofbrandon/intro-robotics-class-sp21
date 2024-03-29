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
        self.pub_cropped = rospy.Publisher("image_cropped", Image, queue_size=10)  # takes compressed image, crops, and publishes to image_cropped
        self.pub_white = rospy.Publisher("image_white", Image, queue_size=10)  # publish to image_white
        self.pub_yellow = rospy.Publisher("image_yellow", Image, queue_size=10)  # publish to image_yellow
        self.pub_masked = rospy.Publisher("image_mask", Image, queue_size=10)  # publish the complete masked image to image_mask

        # these should be the edge detection topics being published
        self.pub_lines_white = rospy.Publisher("image_lines_white", Image, queue_size=10)  # publish to image_lines_white
        self.pub_lines_yellow = rospy.Publisher("image_lines_yellow", Image, queue_size=10)  # publish to image_lines_yellow

        rospy.Subscriber("image_white", Image, self.cb_white)  # subscribe
        rospy.Subscriber("image_yellow", Image, self.cb_yellow)  # subscribe

        self.bridge = CvBridge()  # used to convert b/t ros and cvimages
        self.canny = 0
        self.cv_cropped = 0

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

    def cb(self, msg):
        # convert to a ros image using the bridge
        cv_image = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")

        # ------ CROPPED IMAGE ------

        # ground projection node asks for 120x160 pixels (LxW), and remove the top 4 pixels from the image
        image_size = (160, 120)
        offset = 40
        new_image = cv2.resize(cv_image, image_size, interpolation=cv2.INTER_NEAREST)
        cv_cropped = new_image[offset:, :]

        # convert new image back to ros in order to publish -- this is not required
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
    rospy.init_node('lanedetector')
    LaneDetector()  # calls class
    rospy.spin()
