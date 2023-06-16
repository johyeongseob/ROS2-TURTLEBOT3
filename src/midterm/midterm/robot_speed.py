#!/usr/bin/env python3
import rclpy
from rclpy import node
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from time import sleep

a=0.0
b=0.0

class RobotSpeed(Node):

	def __init__(self):
		super().__init__("robot_speed")
		qos_profile = QoSProfile(depth=10)
		self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
		self.pub2 = self.create_publisher(Float64MultiArray, 'speed_topic', qos_profile)
		self.create_timer(1, self.robot_speed)
		self.create_timer(1, self.input_speed)

	def input_speed(self):
		num = Float64MultiArray()
		global a, b
		a=float(input('vel value: '))  # 단위: m/sec
		b=float(input('anuglar vel value: '))
		#sleep(1)
		num.data = [a, b]
		self.get_logger().info('speed: %s, %s' % (a, b))
		self.pub2.publish(num)

	def robot_speed(self):
		msg = Twist()
		msg.linear.x = a
		msg.angular.z = b
		self.pub.publish(msg)


		
def main(args=None):
	rclpy.init(args=args)                 						 # ROS2 통신을 초기화
	node = RobotSpeed()						     	    	     # 클래스 지정
	rclpy.spin(node)					 						 # 노드가 살아있게 함.
	rclpy.shutdown()                    			 			 # ROS2 통신 종료

if __name__ == "__main__":
	main()								 			 			 # 메인함수 생성