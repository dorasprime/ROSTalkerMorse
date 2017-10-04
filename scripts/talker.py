#!/usr/bin/env python
"""OpenCV feature detectors with ros CompressedImage Topics in python.

This example subscribes to a ros topic containing sensor_msgs
CompressedImage. It converts the CompressedImage into a numpy.ndarray,
then detects and marks features in that image. It finally displays
and publishes the new image - again as CompressedImage topic.
"""
__author__ = 'Mustafa KILINC <mustafa.kilinc at ieee.metu.edu.tr>'
__version__ = '0.1'
__license__ = 'BSD'

# python libs
import sys, time
import rospy
import yaml
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo

global pub1
global pub2
global pub3
global pub4
global pub5
camera_info = CameraInfo()
rgb_camera_info = CameraInfo()
depth_image = Image()
rgb_image = Image()


def callback_depth_camera_info(camera_info_msg):
    global camera_info
    if not rospy.is_shutdown():
        camera_info = camera_info_msg


def callback_depth_image(depth_image):
    global camera_info
    # print("Received a depth image!")
    if not rospy.is_shutdown():
        # depth_image = "hello world %s" % rospy.get_time()
        # rospy.loginfo(depth_image)
        pub2.publish(depth_image)
        pub1.publish(camera_info)


def callback_rgb_camera_info(data_rgb):
    global rgb_camera_info
    if not rospy.is_shutdown():
        rgb_camera_info = data_rgb
        # print("Received a depth image!")
        # #rgb_image = "hello world %s" % rospy.get_time()
        # rospy.loginfo(rgb_image)


def callback_rgb_image(rgb_image):
    global rgb_camera_info
    # print("Received a depth image!")
    if not rospy.is_shutdown():
        # rgb_image = "hello world %s" % rospy.get_time()
        # rospy.loginfo(rgb_image)
        pub4.publish(rgb_image)
        pub3.publish(rgb_camera_info)


def listener():
    rospy.Subscriber("/robot/torso/head/Kinect/depth/camera_info", CameraInfo, callback_depth_camera_info)
    rospy.Subscriber("/robot/torso/head/Kinect/depth/image", Image, callback_depth_image)
    rospy.Subscriber("/robot/torso/head/Kinect/rgb/image", Image, callback_rgb_image)
    rospy.Subscriber("/robot/torso/head/Kinect/rgb/camera_info", CameraInfo, callback_rgb_camera_info)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':


    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    # Depth camera
    pub1 = rospy.Publisher('/camera/depth/camera_info', CameraInfo, queue_size=10)
    pub2 = rospy.Publisher('/camera/depth/image_raw', Image, queue_size=10)
    # rgb camera
    pub3 = rospy.Publisher('/camera/rgb/camera_info', CameraInfo, queue_size=10)
    pub4 = rospy.Publisher('/camera/rgb/image_raw', Image, queue_size=10)

    try:
        listener()
    except rospy.ROSInterruptException:
        pass
