"""
Author: Tyerone Chen
Last Update: 11/72025
"""
# imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from python_qt_binding.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QGridLayout
from python_qt_binding.QtCore import Signal, Slot

class RangeWidget(QWidget):
    # Vars
    value_signal = Signal(float, int)
    SUBSCRIPTION_TO = '/rov/range' # change later, tester
    # constructor
    def __init__(self):
        super().__init__()
        # Node Definement
        self.node = rclpy.create_node('range_widget_node')
        # Widget Setup
        self.title_label = QLabel("Sensor Range:")
        self.value_label = QLabel("N/A")
        self.value_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        self.bar = QProgressBar()
        # Default range
        self.bar.setRange(0, 100)
        self.bar.setFormat("")
        # Widget layout Setup
        layout = QGridLayout()
        layout.addWidget(self.title_label, 0, 0)
        layout.addWidget(self.value_label, 0, 1)
        layout.addWidget(self.bar, 1, 0, 1, 2)
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
        # Connect custom signal to bar
        self.value_signal.connect(self.update_progress_bar)
        self.value_signal.connect(self.update_value_label)
        # Subscription
        self.subscription = self.node.create_subscription(Float32, self.SUBSCRIPTION_TO, self.callback, 10)
    # callback crap
    def callback(self, msg):
        # prob do some more funky math stuff here
        val = max(0.0, min(100.0, msg.data)) # clamp from 0-100
        int_val = int(val)
        self.value_signal.emit(msg.data, int_val)
    @Slot(float, int) # what main thread runs
    def update_progress_bar(self, raw_value, clamped_value):
        self.bar.setValue(clamped_value)
    @Slot(float, int)
    def update_value_label(self, raw_value, clamped_value):
        self.value_label.setText(f"{raw_value:.2f} ({clamped_value}%)")
    # shutdown process
    def shutdown(self):
        if self.node:
            self.node.destroy_node()
