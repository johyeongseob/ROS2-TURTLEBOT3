import rclpy
import math
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import Float64MultiArray
from time import sleep

# vel=0.0; rot=0.0
d1=[]; d2=[]; d3=[]; mindist1=0; mindist2=0; mindist3=0; angle1=0; angle2=0; angle3=0   # 전역변수 초기화

class Command(Node):									 	                              # 클래스 생성, 클래스이름: command

    def __init__(self):					 			 			                          # 클래스 구조 생성
        super().__init__('command')		 			 		                              # 노드 이름 지정: robot_news_station. 노드이름과 파일이름은 다르다.

        qos_profile = QoSProfile(depth=10)
        # self.subscription1 = self.create_subscription(Int16MultiArray, 'angle', self.lidar_range, qos_profile)    
                                                                                          # subscriber 생성(메세지타입, 토픽이름, 콜백(수신한 메세지를 처리), 대기열크기)
        self.subscription2 = self.create_subscription(LaserScan, '/scan', self.min_distance, qos_profile_sensor_data)
        # self.subscription3 = self.create_subscription(Float64MultiArray, 'speed', self.motor_callback, qos_profile_sensor_data)
        self.pubulisher1 = self.create_publisher(Twist, '/cmd_vel', 10)                     # class의 publisher속성 생성 (메세지타입, 토픽이름, 대기열크기)
        self.create_timer(1, self.controller)
        self.get_logger().info('Start!')

    # def lidar_range(self,msg):
    #     global angle1, angle2
    #     angle1 = msg.data[0]                                                              # 장애물 감지 범위 왼쪽
    #     angle2 = msg.data[1]                                                              # 장애물 감지 범위 오른쪽
    #     self.get_logger().info('Change anlges: %s to %s' % (angle1, angle2))

    def min_distance(self,msg):
        global d1, d2, d3, mindist1, mindist2, mindist3, angle1, angle2, angle3

        for i in range(-40, 60):
            dist = msg.ranges[i]*100
            if dist == 0:
                 dist = 99.9
            if i <-20:
                d1.append(dist)
                mindist1 = min(d1)
                angle1 = d1.index(mindist1)-60
            elif i <20+1:
                d2.append(dist)
                mindist2 = min(d2)
                angle2 = d2.index(mindist2)-20
            else:
                d3.append(dist)
                mindist3 = min(d3)
                angle3 = d3.index(mindist3)+20
                
        d1=[]; d2=[]; d3=[]

    # def motor_callback(self, msg):
    #     global vel, rot
    #     vel = msg.data[0]                                                                  # 전진 
    #     rot = msg.data[1]                                                                  # 회전

    def controller(self):
        msg = Twist()                                                                      # 메세지타입
        vel=0.1
        rot=0.3
        msg.linear.x = vel                                                               # 전진
        msg.angular.z = rot                                                         # 좌회전
        self.pubulisher1.publish(msg)

        # if mindist1 < 15:
        #     self.get_logger().info('alert right bumping. at %s angle, distance = %s' % (angle3, mindist1))
        #     msg.linear.x -= vel  
        #     msg.angular.z += 0.2
        #     self.pubulisher1.publish(msg)

        #     if mindist2 < 15:
        #         msg.angular.z += 0.3
        #         self.pubulisher1.publish(msg)

        if mindist3 < 20:
            self.get_logger().info('alert left bumping. at %s angle, distance = %s' % (angle1, mindist3))
            msg.linear.x -= vel
            msg.angular.z -= 0.5

            self.pubulisher1.publish(msg)

            if mindist2 < 20:
                msg.angular.z -= 0.3
                self.pubulisher1.publish(msg)

        elif mindist2 < 20:
            msg.linear.x -= vel                                                          # 정지  
            msg.angular.z -= 0.6
            self.pubulisher1.publish(msg)

                   


def main(args=None):
    rclpy.init(args=args)                 						                            # ROS2 통신을 초기화
    node = Command()						     	    	                                # 클래스 지정
    try :
        rclpy.spin(node)					 					                   	        # 노드가 살아있게 함.
    except KeyboardInterrupt :
        node.get_logger().info('Stopped by Keyboard')
    finally :
        node.destroy_node()
        rclpy.shutdown()                    			 			                        # ROS2 통신 종료

if __name__ == '__main__':
    main()								 			 		                     	        # 메인함수 생성