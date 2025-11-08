# imports
import math
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

class SimPublisher(Node):
    # vars
    RANGE_PUB_NAME = 'rov/range'
    DATA_PUB_NAME = 'rov/data'
    TIMER_INTERVAL = 0.1
    # constructor
    def __init__(self):
        super().__init__('simple_simpub')
        # publisher creator
        self.range_pub = self.create_publisher(Float32, self.RANGE_PUB_NAME, 10)
        self.data_pub = self.create_publisher(String, self.DATA_PUB_NAME, 10)
        # timer setup
        self.timer = self.create_timer(self.TIMER_INTERVAL, self.timer_callback)
        # logger
        self.get_logger().info(f'Simulation Publisher Node Started...')
        self.counter = 0

    def timer_callback(self):
        # Range Publisher Data
        # Creates a nice ocislation whatever, idk i looked this one up
        sim_range = 50.0 + 40.0 * math.sin(self.counter * 0.1) 
        noise = random.uniform(-1.0, 1.0)
        final_range = sim_range + noise
        range_msg = Float32()
        range_msg.data = final_range
        self.range_pub.publish(range_msg)
        # Data Display Publisher
        if self.counter % 100 == 0:
            # got bored lol
            states = ["good", 
                      "good..?", 
                      "goody goody goo", 
                      "goodn't",
                      "ungood",
                      "gouda"]
            data_msg = String()
            data_msg.data = random.choice(states)
            self.data_pub.publish(data_msg)
        self.counter += 1
    
def main(args=None):
    rclpy.init(args=args)
    sim_publisher = SimPublisher()
    rclpy.spin(sim_publisher)
    sim_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
