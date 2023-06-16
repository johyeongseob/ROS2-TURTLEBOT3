import rclpy
from rclpy import node
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Int8MultiArray
import datetime as dt

class FirstPub(Node):
    
    def __init__(self):
        super().__init__('first_pub')

        qos_profile = QoSProfile(depth=10)
        self.counter = 1
        self.pub = self.create_publisher(Int8MultiArray, 'first_topic', qos_profile)
        self.timer = self.create_timer(1, self.first_publisher)
        self.get_logger().info("First publisher has been started.")

    def first_publisher(self):
        num = Int8MultiArray()
        time = dt.datetime.now()
        self.get_logger().info("시간: " + str(time) + "  " + str(self.counter) + "번째 데이터")
        num1 = int(input('첫 번째 숫자를 입력하세요: '))
        num2 = int(input('두 번째 숫자를 입력하세요: '))
        num3 = int(self.counter)
        num.data = [num1, num2, num3]
        self.counter += 1
        self.pub.publish(num)


def main(args=None):
  rclpy.init(args=args)
  node = FirstPub()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard Interrupt (SIGINT)')
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()