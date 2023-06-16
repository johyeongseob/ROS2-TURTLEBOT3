import rclpy
import math
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from time import sleep

d1=0; d2=0    #전역변수 초기화

class ImuSubscriber(Node):

    def __init__(self):
        super().__init__('Imu_subscriber')

        self.previous_angle=0
        self.subscription = self.create_subscription(Imu, '/imu', self.listener_callback_imu, qos_profile=qos_profile_sensor_data)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.listener_callback_scan, qos_profile_sensor_data)

    def listener_callback_imu(self, msg):
        
        x=msg.orientation.x
        y=msg.orientation.y
        z=msg.orientation.z
        w=msg.orientation.w

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        X = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.degrees(math.asin(t2))
        
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        Z = math.degrees(math.atan2(t3, t4))

        if Y > 30 and self.previous_angle <= 30:
            self.previous_angle = Y
            self.get_logger().info('IMU angle is upper than 30 degree front now')
        if Y < -30 and self.previous_angle >= -30:
            self.previous_angle = Y
            self.get_logger().info('IMU angle is lower than -30 degree behind now')

        if Y > 30:
            sleep(0.5)
            self.get_logger().info('Lidar range: %s' % d1)
        if Y < -30:
            sleep(0.5)
            self.get_logger().info('Lidar range: %s' % d2)

    def listener_callback_scan(self,msg):
        global d1, d2
        d1=msg.ranges[0]
        d2=msg.ranges[180]

def main(args=None):
    rclpy.init(args=args)
    node = ImuSubscriber()
    try :
        while rclpy.ok():
            rclpy.spin_once(node)
    except KeyboardInterrupt :
        node.get_logger().info('Stopped by Keyboard')
    finally :
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()