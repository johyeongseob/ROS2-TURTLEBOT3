import rclpy
import math
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Float64MultiArray
from time import sleep

a=0.0; b=0.0; c=-180; d=180; Y=0; d1=[]; d2=[]; d3=[]; d4=[]; mindist2=0; mindist3=0; mindist4=0

class RobotWindow(Node):

    def __init__(self):
        super().__init__('robot_window')
        qos_profile = QoSProfile(depth=10)
        self.subscription1 = self.create_subscription(Int16MultiArray, 'angle', self.read_angle, qos_profile)
        self.subscription2 = self.create_subscription(LaserScan, '/scan', self.listener_callback_scan, qos_profile_sensor_data)
        self.subscription3 = self.create_subscription(Imu, '/imu', self.listener_callback_imu, qos_profile=qos_profile_sensor_data)
        self.subscription4 = self.create_subscription(Float64MultiArray, 'speed_topic', self.listener_callback_motor, qos_profile_sensor_data)
        self.pubulish1 = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_timer(1, self.controller)
    
    def read_angle(self,msg):
        global c, d
        c = msg.data[0]
        d = msg.data[1]
        self.get_logger().info('Change anlges: %s to %s' % (c, d))
        sleep(2)

    def listener_callback_scan(self,msg):
        global d1, d2, d3, d4, mindist2, mindist3, mindist4
        
        for i in range(c, d+1):
            dist = msg.ranges[i]*100
            if dist == 0:
                 dist = 99.9
            d1.append(dist)
            mindist = min(d1)
            angle = d1.index(mindist)+c
        self.get_logger().info('at %s angle, minimum distance: %s' % (angle, mindist))
        sleep(1)
        d1=[]

        for j in range(c,d+1):
            dist = msg.ranges[j]*100
            if dist == 0:
                dist = 99.9
            if j <- 20:
                    d2.append(dist)
                    mindist2 = min(d2)
            elif j < 21:
                    d3.append(dist)
                    mindist3 = min(d3)
            else:
                    d4.append(dist)
                    mindist4 = min(d4)                
        d2=[]; d3=[]; d4=[]

    def listener_callback_imu(self, msg):
        global X, Y, Z
        
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

    def listener_callback_motor(self, msg):
        global a, b
        a = msg.data[0]
        b = msg.data[1]

    def controller(self):
        msg = Twist()

        if Y > 60 or Y < -60:
            self.get_logger().info('robot slip. Y value = %s' %Y)
            msg.linear.x = 0.0 
            msg.angular.z = 0.0
            self.pubulish1.publish(msg)
        else:
            msg.linear.x = a
            msg.angular.z = b
            self.pubulish1.publish(msg)

            if mindist2 < 20:
                self.get_logger().info('alert right bumping. right distance = %s' %mindist2)
                msg.angular.z += 0.1
                self.pubulish1.publish(msg)

            if mindist3 < 20:
                self.get_logger().info('alert front bumping. front distance = %s' %mindist3)
                msg.linear.x -= a
                msg.angular.z -= b
                self.pubulish1.publish(msg)

            if mindist4 < 20:
                self.get_logger().info('alert left bumping. left distance = %s' %mindist4)
                msg.angular.z -= 0.1
                self.pubulish1.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotWindow()
    try :
        rclpy.spin(node)
    except KeyboardInterrupt :
        node.get_logger().info('Stopped by Keyboard')
    finally :
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()