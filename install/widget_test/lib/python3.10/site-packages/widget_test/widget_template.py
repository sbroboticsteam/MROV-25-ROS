"""
Author: Tyerone Chen
Last Update: 11/72025
"""
# imports
import rclpy
from rqt_gui_py.plugin import Plugin
from python_qt_binding.QtWidgets import QWidget, QVBoxLayout, QSplitter
from python_qt_binding.QtCore import Qt
from threading import Thread
from rclpy.executors import MultiThreadedExecutor
# Custom Widgets
from .camera_widget import CameraWidget
from .range_widget import RangeWidget
from .data_display_widget import DataDisplayWidget

class WidgetTemplate(Plugin):
    # constructor
    def __init__(self, context):
        # Renamed from MyRqtTest to WidgetTemplate
        super(WidgetTemplate, self).__init__(context)
        self.setObjectName('WidgetTemplate')
        
        # Setsups ROS2 if it hasn't
        if not rclpy.ok():
            rclpy.init(args=None)
        # setup multu threader
        self.executor = MultiThreadedExecutor()
        # setup main widget
        self.main_widget = QWidget()
        self.vertical_splitter = QSplitter(Qt.Vertical)
        self.horizontal_splitter = QSplitter(Qt.Horizontal)
        # Init custom widgets
        self.camera_widget = CameraWidget()
        self.range_widget = RangeWidget()
        self.data_widget = DataDisplayWidget()
        self.executor.add_node(self.camera_widget.node)
        self.executor.add_node(self.range_widget.node)
        self.executor.add_node(self.data_widget.node)
        # Add widgets to splitters
        self.horizontal_splitter.addWidget(self.range_widget)
        self.horizontal_splitter.addWidget(self.data_widget)
        self.vertical_splitter.addWidget(self.camera_widget)
        self.vertical_splitter.addWidget(self.horizontal_splitter)
        self.vertical_splitter.setSizes([200, 100]) # ratio setter -> 2:1 use in 100s
        #self.horizontal_splitter.setSizes([100, 300]) #
        layout = QVBoxLayout()
        layout.addWidget(self.vertical_splitter)
        self.main_widget.setLayout(layout)
        # handle multiple instances
        title = "ROS 2 Widget Template"
        if context.serial_number() > 1:
            self.main_widget.setWindowTitle(f"{title} ({context.serial_number()})")
        else:
            self.main_widget.setWindowTitle(title)
        context.add_widget(self.main_widget)
        # thread setup
        self.spin_thread = Thread(target=self.executor.spin, daemon=True)
        self.spin_thread.start()

    # shutdown process
    def shutdown_plugin(self):
        self.camera_widget.shutdown()
        self.range_widget.shutdown()
        self.data_widget.shutdown()

        if self.executor:
            self.executor.shutdown()
        if rclpy.ok():
             rclpy.shutdown()