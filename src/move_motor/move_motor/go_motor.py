#!/usr/bin/env python3
import rclpy
from rclpy import node
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
from std_msgs.msg import String
from time import sleep

d1=0
d2=0
d3=0
a=0.0
b=0.0

class GoMotor(Node):

	def __init__(self):
		super().__init__("motor_pub")

		self.previous_range1=0
		self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
		self.sub = self.create_subscription(LaserScan, '/scan', self.listener_callback_scan, qos_profile_sensor_data)
		self.get_logger().info("move_start")
		self.create_timer(1, self.go_motor)	 			 # 타이머 생성(간격, 타이머함수)

	def listener_callback_scan(self,msg):
		global d1, d2, d3
		d1=msg.ranges[0]*100
		d2=msg.ranges[45]*100
		d3=msg.ranges[315]*100

	def go_motor(self):
		msg = Twist()

		global d1, d2, d3
		if d1 == 0:	d1=99.9
		if d2 == 0:	d2=99.9
		if d3 == 0:	d3=99.9

		if d1 > 20 and self.previous_range1 <= 20:
			self.previous_range1 = d1
			global a, b
			a=float(input('vel value: '))  # 단위: m/sec
			b=float(input('anuglar vel value: '))
			sleep(1)

		msg.linear.x = a
		msg.angular.z = b
		self.pub.publish(msg)
		
		if d1 < 20:
			msg.linear.x = 0.0
			msg.angular.z = 0.0
			self.pub.publish(msg)
		else:
			msg.linear.x = a
			msg.angular.z = b
			self.pub.publish(msg)

		self.get_logger().info('I heard: three ranges front, right45, left45 = %s, %s, %s' % (d1, d2, d3))
		sleep(0.5)



def main(args=None):
	rclpy.init(args=args)                 						 # ROS2 통신을 초기화
	node = GoMotor()						     	    	     # 클래스 지정
	rclpy.spin(node)					 						 # 노드가 살아있게 함.
	rclpy.shutdown()                    			 			 # ROS2 통신 종료

if __name__ == "__main__":
	main()								 			 			 # 메인함수 생성