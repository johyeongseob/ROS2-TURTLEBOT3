#!/usr/bin/env python3
import rclpy
from rclpy import node
from rclpy.node import Node             			 	         		  # 노드클래스로부터 노드를 가져온다.

from example_interfaces.msg import String                                 # package.xml에 새로운 종속성 추가


class RobotNewsStationNode(Node):									 	  # 클래스 생성, 클래스이름: RobotNewsStationNode
    def __init__(self):					 			 			          # 클래스 구조 생성
        super().__init__("robot_news_station")		 			 		  # 노드 이름 지정: robot_news_station. 노드이름과 파일이름은 다르다.

        self.robot_name_ = "johs"
        self.publisher_ = self.create_publisher(String, "robot_news", 10) # class의 publisher속성 생성 (메세지타입, 토픽이름, 대기열크기)
        self.timer_ = self.create_timer(0.5, self.publish_news)
        self.get_logger().info("Robot News station has been started ") 	  # print Robot News station has been started

    def publish_news(self):
        msg = String()
        msg.data = "Hi, this is " + str(self.robot_name_) + "from the robot news station."
        self.publisher_.publish(msg)                                      # message를 publish하기 위해 publish method를 생성. 함수 호출 시, 주제에 대한 메세지가 publish.

def main(args=None):
    rclpy.init(args=args)
    node = RobotNewsStationNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()