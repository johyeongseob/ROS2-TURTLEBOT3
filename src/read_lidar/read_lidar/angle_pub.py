import rclpy
from rclpy import node
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Int16MultiArray

class AnglePub(Node):
    
    def __init__(self):
        super().__init__('angle_pub')

        qos_profile = QoSProfile(depth=10)
        self.counter = 1
        self.pub = self.create_publisher(Int16MultiArray, 'angle', qos_profile)
        self.timer = self.create_timer(1, self.angle_pub)
        self.get_logger().info("Anlge publisher is now ready!")

    def angle_pub(self):
        num = Int16MultiArray()
        self.get_logger().info(str(self.counter) + "번째 데이터")
        num1 = int(input('첫 번째 각도를 입력하세요: '))
        num2 = int(input('두 번째 각도를 입력하세요: '))
        num.data = [num1, num2]
        self.counter += 1
        self.pub.publish(num)


def main(args=None):
  rclpy.init(args=args)
  node = AnglePub()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard Interrupt (SIGINT)')
  finally:
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
  main()