"""
Author: Tyerone Chen
Last Update: 11/72025
"""
# imports
import rclpy
import cv2
import time
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge # Used for converting image types

class CameraPublisher(Node):
    # Vars
    TOPIC_NAME = '/rov/camera/image_raw'
    TIMER_INTERVAL = 0.1
    
    # Constructor
    def __init__(self):
        super().__init__('simple_campub')
        self.pub = self.create_publisher(Image, self.TOPIC_NAME, 10)
        self.timer = self.create_timer(self.TIMER_INTERVAL, self.timer_callback)
        self.bridge = CvBridge() 
        # init video capture
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.capture_failed = False
        if not self.cap.isOpened(): # chedcker to see if this shit failed becausea sljdaljds
            self.get_logger().error("Couldn't Open video Stream")
            self.capture_failed = True 
        else:
            self.get_logger().info("Publishing Node Started")
            time.sleep(0.5)
            ret, frame = self.cap.read()
            if not ret:
                self.get_logger().warn("Initial camera read failed - setting capture_failed to True.")
                self.capture_failed = True
    # callback waterver
    def timer_callback(self):
        if self.capture_failed:
            return
        ret, frame = self.cap.read() 
        
        if ret:
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            img_msg.header.stamp = self.get_clock().now().to_msg()
            img_msg.header.frame_id = 'camera_frame'
            self.pub.publish(img_msg) 

    # shutdown thingy
    def shutdown(self):
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()
# main
def main(args=None):
    rclpy.init(args=args)
    cam_pub = CameraPublisher()
    
    try:
        rclpy.spin(cam_pub)
    except KeyboardInterrupt:
        pass
    finally:
        cam_pub.shutdown()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
