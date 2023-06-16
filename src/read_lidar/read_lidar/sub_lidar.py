import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
from time import sleep

b=0; c=0

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        
        self.previous_range1=0
        self.previous_range2=0
        qos_profile = QoSProfile(depth=10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback_scan, qos_profile_sensor_data)
        self.anglesub = self.create_subscription(Int16MultiArray, 'angle', self.read_angle, qos_profile)
    
    def read_angle(self,msg):
        global b, c
        b = msg.data[0]
        c = msg.data[1]
        self.get_logger().info('I heard 2 anlges: ' + str(b) + "', " + str(c) + "'" + "  Please wait a minute")
        for t in [3, 2, 1, 0]:
            sleep(2/3)
            self.get_logger().info('Count %s' %t)


    def listener_callback_scan(self,msg):
        d1=msg.ranges[b]*100
        d2=msg.ranges[c]*100
        
        self.get_logger().info('I heard: range1: %s, range2: %s' % (d1,d2))
        sleep(0.5)

        if d1 < 40 and self.previous_range1 >= 40:
            self.previous_range1 = d1
            self.get_logger().info('This range1 is lower than 40cm')
            sleep(1)
        elif d1 > 40 and self.previous_range1 <= 40:
            self.previous_range1 = d1
            self.get_logger().info('This range1 is upper than 40cm')
            sleep(1)

        if d2 < 40 and self.previous_range2 >= 40:
            self.previous_range2 = d2
            self.get_logger().info('This range2 is lower than 40cm')
            sleep(1)
        elif d2 > 40 and self.previous_range2 <= 40:
            self.previous_range2 = d2
            self.get_logger().info('This range2 is upper than 40cm')
            sleep(1)

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    try :
        rclpy.spin(node)
    except KeyboardInterrupt :
        node.get_logger().info('Stopped by Keyboard')
    finally :
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()