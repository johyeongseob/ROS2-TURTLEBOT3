import rclpy
from rclpy import node
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from std_msgs.msg import Int8MultiArray
from time import sleep

class FirstSub(Node):
    
    def __init__(self):
        super().__init__('first_sub')

        qos_profile = QoSProfile(depth=10)
        self.sub = self.create_subscription(Int8MultiArray, 'first_topic', self.first_subscriber, qos_profile)
        self.get_logger().info("First subscriber has been started.")

    def first_subscriber(self, msg):
        b = msg.data[0]
        c = msg.data[1]
        d = msg.data[2]
        sleep(0.3)
        self.get_logger().info(str(d) + " 번째 데이터: " + str(b) + " + " + str(c) + " = " + str(b+c))


def main(args=None):
  rclpy.init(args=args)
  node = FirstSub()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard Interrupt (SIGINT)')
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()