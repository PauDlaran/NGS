#!/usr/bin/env python3

import cv2
import depthai as dai
import time
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# Initialize ROS node
rospy.init_node('depthai_camera_publisher', anonymous=True)

# Set the topic name
ros_topic = "/cam1"

# Create a publisher for the image topic
image_publisher = rospy.Publisher(ros_topic, Image, queue_size=10)

# Create CvBridge
bridge = CvBridge()

# Connect to device and start pipeline
with dai.Device() as device:
    # Create pipeline
    pipeline = dai.Pipeline()
    cams = device.getConnectedCameraFeatures()
    streams = []
    for cam in cams:
        print(str(cam), str(cam.socket), cam.socket)
        c = pipeline.create(dai.node.Camera)
        x = pipeline.create(dai.node.XLinkOut)
        c.preview.link(x.input)
        c.setBoardSocket(cam.socket)
        stream = str(cam.socket)
        if cam.name:
            stream = f'{cam.name} ({stream})'
        x.setStreamName(stream)
        streams.append(stream)

    # Start pipeline
    device.startPipeline(pipeline)
    fpsCounter = {}
    lastFpsCount = {}
    tfps = time.time()
    
    while not device.isClosed():
        queueNames = device.getQueueEvents(streams)
        for stream in queueNames:
            messages = device.getOutputQueue(stream).tryGetAll()
            fpsCounter[stream] = fpsCounter.get(stream, 0.0) + len(messages)
            for message in messages:
                # Display arrived frames
                if type(message) == dai.ImgFrame:
                    # render fps
                    fps = lastFpsCount.get(stream, 0)
                    frame = message.getCvFrame()
                    cv2.putText(frame, "Fps: {:.2f}".format(fps), (10, 10), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (255,255,255))
                    
                    # Convert OpenCV image to ROS Image message
                    ros_image_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                    
                    # Publish the ROS Image message
                    image_publisher.publish(ros_image_msg)

        if time.time() - tfps >= 1.0:
            scale = time.time() - tfps
            for stream in fpsCounter.keys():
                lastFpsCount[stream] = fpsCounter[stream] / scale
            fpsCounter = {}
            tfps = time.time()

        if cv2.waitKey(1) == ord('q'):
            break

# Cleanup
cv2.destroyAllWindows()
