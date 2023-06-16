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

vel=0.0; rot=0.0

class MotorControl(Node):

	def __init__(self):
		super().__init__("motor_control")
		qos_profile = QoSProfile(depth=10)
		# self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
		self.pub2 = self.create_publisher(Float64MultiArray, 'speed', qos_profile)
		# self.create_timer(1, self.motor_speed)
		self.create_timer(1, self.input_speed)

	def input_speed(self):
		num = Float64MultiArray()
		global vel, rot
		vel=float(input('vel value: '))  # 단위: m/sec
		rot=float(input('anuglar vel value: '))
		num.data = [vel, rot]
		self.get_logger().info('speed: %s, %s' % (vel, rot))
		self.pub2.publish(num)

	# def motor_speed(self):
	# 	msg = Twist()
	# 	msg.linear.x = x
	# 	msg.angular.z = z
	# 	self.pub.publish(msg)


		
def main(args=None):
	rclpy.init(args=args)                 						 # ROS2 통신을 초기화
	node = MotorControl()						     	    	 # 클래스 지정
	rclpy.spin(node)					 						 # 노드가 살아있게 함.
	rclpy.shutdown()                    			 			 # ROS2 통신 종료

if __name__ == "__main__":
	main()								 			 			 # 메인함수 생성