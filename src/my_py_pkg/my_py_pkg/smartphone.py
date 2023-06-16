#!/usr/bin/env python3
import rclpy
from rclpy import node
from rclpy.node import Node

from example_interfaces.msg import String


class SmartPhoneNode(Node):
    def __init__(self):
        super().__init__("smartphone")
        self.subscriber_ = self.create_subscription(String, "robot_news", self.callback_robot_news, 10) 
        # subscriber 생성(메세지타입, 토픽이름<-같아야 동기화, 콜백(수신한 메세지를 처리), 대기열크기)
        self.get_logger().info("Smartphone has been started.")

    def callback_robot_news(self,msg):
        self.get_logger().info(msg.data)    # publisher에서 보낸 message를 받아서 print한다.


def main(args=None):
    rclpy.init(args=args)
    node = SmartPhoneNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()