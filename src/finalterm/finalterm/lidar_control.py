import rclpy
from rclpy import node
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Int16MultiArray

class LidarControl(Node):
    
    def __init__(self):
        super().__init__('lidar_control')

        qos_profile = QoSProfile(depth=10)
        self.pub = self.create_publisher(Int16MultiArray, 'angle', qos_profile)
        self.timer = self.create_timer(1, self.lidar_angle)

    def lidar_angle(self):
        num = Int16MultiArray()
        angle1 = int(input('첫 번째 각도를 입력하세요: '))
        angle2 = int(input('두 번째 각도를 입력하세요: '))
        num.data = [angle1, angle2]
        self.get_logger().info('angles: %s, %s' % (angle1, angle2))
        self.pub.publish(num)

def main(args=None):
  rclpy.init(args=args)
  node = LidarControl()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    node.get_logger().info('Keyboard Interrupt (SIGINT)')
  finally:
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
  main()