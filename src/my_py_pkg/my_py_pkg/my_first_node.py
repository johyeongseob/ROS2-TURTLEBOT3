#!/usr/bin/env python3
import rclpy
from rclpy import node
from rclpy.node import Node             			 			 # 노드클래스로부터 노드를 가져온다.

class MyNode(Node):									 			 # 클래스 생성, 클래스이름: MyNode

	def __init__(self):					 			 			 # 클래스 구조 생성
		super().__init__("py_test")		 			 			 # 노드 이름 지정: py_test 노드이름과 파일이름은 다르다.
		self.counter_ = 0							 			 # counter를 0으로 초기화
		self.get_logger().info("Hello ROS2!!!")  	 			 # print Hello ROS2
		self.create_timer(0.5, self.timer_callback)	 			 # 타이머 생성(간격, 타이머함수)
	
	def timer_callback(self):			  			 			 # 타이머함수: 일정간격으로 실행
		self.counter_ += 1
		self.get_logger().info("Hello " + str(self.counter_))    # '+'를 사용하여 여러 인수를 입력 

def main(args=None):
	rclpy.init(args=args)                 						 # ROS2 통신을 초기화
	node = MyNode()						     	    			 # 클래스 지정
	rclpy.spin(node)					 						 # 노드가 살아있게 함.
	rclpy.shutdown()                    			 			 # ROS2 통신 종료
	
if __name__ == "__main__":
	main()								 			 			 # 메인함수 생성