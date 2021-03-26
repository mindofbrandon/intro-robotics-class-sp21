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


class ImageProcess:
    def __init__(self):
        rospy.Subscriber("image", Image, self.cb)  # subscribe
        self.pub_cropped = rospy.Publisher("image_cropped", Image, queue_size=10)  # publish to image_cropped
        self.pub_white = rospy.Publisher("image_white", Image, queue_size=10)  # publish to image_white
        self.pub_yellow = rospy.Publisher("image_yellow", Image, queue_size=10)  # publish to image_yellow
        self.pub_masked = rospy.Publisher("image_mask", Image, queue_size=10)  # publish the complete masked image to image_mask
        self.bridge = CvBridge()  # used to convert b/t ros and cvimages

        # roslaunch image_processing_hw image_pub.launch index:=2
        # change index number if you wanna try with another image

    def cb(self, msg):
        # convert to a ros image using the bridge
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # access pixel value through array indexing (not needed for this homework)
        # pixel = cv_image[i,j,k]

        # ------ CROPPED IMAGE AND PUBLISHING ------

        # crop top half of image
        # sample image dimensions:
        # width = 640 pixels
        # height = 480 pixels

        # cv_cropped = cv_image[start_y:end_y, start_x:end_x]
        cv_cropped = cv_image[240:480, 0:640]  # first value is height, so it should crop half the image
        # 0:240 prints the top half, oops

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

        # mask both images
        # OR both images to get both grayscales together
        mask_white = cv2.bitwise_or(cv_white, cv_white)

        # erode and shrink to get cleaner image
        kernel_white = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        image_erode = cv2.erode(cv_cropped, kernel_white)
        # what should be done here?


        # AND both images to get color back
        output_white = cv2.bitwise_and(cv_cropped, cv_cropped, mask=mask_white)

        # convert new image back to ros in order to publish
        ros_white_final = self.bridge.cv2_to_imgmsg(output_white, "bgr8")

        # publish edited image
        self.pub_white.publish(ros_white_final)

        # ------ YELLOW MASK AND PUBLISHING ------

        cv_yellow = cv2.inRange(hsv_image, (27, 50, 150), (30, 255, 255))

        # mask both images
        # OR both images to get both grayscales together
        mask_yellow = cv2.bitwise_or(cv_yellow, cv_yellow)

        # AND both images to get color back
        output_yellow = cv2.bitwise_and(cv_cropped, cv_cropped, mask=mask_yellow)

        # convert new image back to ros in order to publish
        ros_yellow_final = self.bridge.cv2_to_imgmsg(output_yellow, "bgr8")

        # publish edited image
        self.pub_yellow.publish(ros_yellow_final)

        # ------ BOTH TOGETHER AND PUBLISHING ------
        # This part was not required, but I kept it so that I could get a better understanding

        # mask both images
        # OR both images to get both grayscales together
        mask = cv2.bitwise_or(cv_white, cv_yellow)

        # AND both images to get color back
        output = cv2.bitwise_and(cv_cropped, cv_cropped, mask=mask)

        # convert new image back to ros in order to publish
        ros_edited = self.bridge.cv2_to_imgmsg(output, "bgr8")

        # publish edited image
        self.pub_masked.publish(ros_edited)


if __name__ == '__main__':
    rospy.init_node('imageprocess')
    ImageProcess()  # calls class
    rospy.spin()
