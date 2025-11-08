"""
Author: Tyerone Chen
Last Update: 11/72025
"""
# imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from python_qt_binding.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from python_qt_binding.QtCore import Signal, Slot

class DataDisplayWidget(QWidget):
    data_signal = Signal(str)

    # constructor
    def __init__(self):
        super().__init__()
        # node & subscription setup
        self.node = rclpy.create_node('data_display_widget_node')
        self.subscription = None
        # widget setup 
        self.topic_label = QLabel("Topic: ")
        self.topic_input = QLineEdit("/rov/data") # change to something else later
        self.subscribe_button = QPushButton("Subscribe!")
        self.data_label = QLabel("No Data Received Yet...")
        self.data_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        # Widget layou setup
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.topic_label)
        top_layout.addWidget(self.topic_input)
        top_layout.addWidget(self.subscribe_button)
        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.data_label)
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
        # Button connection
        self.subscribe_button.clicked.connect(self.subscribe_to_topic)
        self.data_signal.connect(self.update_data_label)

    def subscribe_to_topic(self):
        topic_name = self.topic_input.text().strip()
        if not topic_name:
            self.data_label.setText("Please Enter a Topic Name")
        if self.subscription: # Subscription destroyer
            self.node.destroy_subscription(self.subscription)
            self.subscription = None
        try:
            self.subscription = self.node.create_subscription(String, topic_name, self.string_callback, 10)
            self.data_label.setText(f"Subscribed to {topic_name} (std_msgs/String)")
        except Exception: # try to subscribe to float32 if string doesn't work
            try:
                self.subscription = self.node.create_subscription(Float32, topic_name, self.float_callback, 10)
                self.data_label.setText(f"Subscribed to {topic_name} (std_msgs/Float32)") 
            except Exception as ex:
                self.data_label.setText(f"Couldn't Subscribe to: {topic_name}| ERROR: {ex}")
    # callbacks
    def string_callback(self, msg):
        display_text = f"String Data: {msg.data}"
        self.data_signal.emit(display_text)
    def float_callback(self, msg):
        # Do som calculation crap here
        display_text = f"Float Data: {msg.data}"
        self.data_signal.emit(display_text)
    @Slot(str) # what main thread runs
    def update_data_label(self, text):
        self.data_label.setText(text)
    # shutdown process
    def shutdown(self):
        if self.node:
            self.node.destroy_node()
