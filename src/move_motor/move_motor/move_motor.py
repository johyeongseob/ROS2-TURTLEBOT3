
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


# getKey() 함수를 사용하기 위한 library들 선언
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

# 키보드 입력을 받기 위한 함수
def getKey():
    if os.name == 'nt':
        timeout = 0.1
        startTime = time.time()
        while(1):
            if msvcrt.kbhit():
                if sys.version_info[0] >= 3:
                    return msvcrt.getch().decode()
                else:
                    return msvcrt.getch()
            elif time.time() - startTime > timeout:
                return ''

    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


"""
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x
w/x : increase/decrease linear velocity 
a/d : increase/decrease angular velocity 
space key, s : force stop

q to quit
"""

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')

        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)     
    
    def pub(self, msg):
        self.publisher_.publish(msg)



def main(args=None):

    rclpy.init(args=args)

    node = MinimalPublisher()
    msg = Twist()
    
    while rclpy.ok():

        key = getKey()      # 한영 확인. 영어로 입력.
        key = key.lower()   # 대문자 입력 시 소문자로 변환

        if key == 'w':      # 전진
            msg.linear.x += 0.05    # 단위: m/sec

        elif key == 'x':    # 후진
            msg.linear.x -= 0.05    # 단위: m/sec

        elif key == 'a':    # 좌회전
            msg.angular.z += 0.2    # 단위: rad/sec

        elif key == 'd':    # 우회전
            msg.angular.z -= 0.2    # 단위: rad/sec

        elif key == 's':    # 정지
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        elif key == 'q':    # 종료
            node.destroy_node()
            rclpy.shutdown()

        node.pub(msg)


if __name__ == '__main__':
    main()