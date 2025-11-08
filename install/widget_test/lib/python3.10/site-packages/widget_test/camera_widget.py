"""
Author: Tyerone Chen
Last Update: 11/72025
"""
# imports
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from python_qt_binding.QtWidgets import QLabel, QVBoxLayout, QWidget
from python_qt_binding.QtCore import QThread, Signal, Slot 
from python_qt_binding.QtGui import QImage, QPixmap

class CameraWidget(QWidget):
    image_signal = Signal(QPixmap)

    # constructor
    def __init__(self):
        # Widget Layout Setup
        super().__init__()
        self.label = QLabel("Waiting for Camera Data...")
        self.label.setScaledContents(True)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        # Style Sheet Crap
        self.setStyleSheet("""
            QWidget {
                border: 2px solid black;
                border-radius: 2.5px;
                padding: 5px;
                margin: 0px;
            }
        """)
        # Connect the custom signal to the update slot
        self.image_signal.connect(self.update_image_label)
        # ROS2 Nod Setup
        self.node = rclpy.create_node('camera_widget_node')
        self.bridge = CvBridge()
        self.sub = self.node.create_subscription(Image, '/rov/camera/image_raw', self.callback, 10)
    # callback crap
    def callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.image_signal.emit(pixmap)
        except Exception as ex:
            self.node.get_logger().error(f"ERROR in camera callback: {ex}")

    @Slot(QPixmap)
    def update_image_label(self, pixmap):
        self.label.setPixmap(pixmap)
    # shutdown process
    def shutdown(self):
        if self.node:
            self.node.destroy_node()
