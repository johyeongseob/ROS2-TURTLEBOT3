# Autonomous_Robot
ROS2 &amp;  TURTLEBOT3

How to set ROS2 on your computer

ros2 humble-desktop 설치
링크: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

install the ROS2 build tool - Colcon
sudo apt install python3-colcon-common-extensions

ROS2 작업 공간 생성
cd(home)
mkdir ros2_ws
cd ros2_ws
mkdir src
colcon build

cd(home)
gedit .bashrc
Line119:source /opt/ros/humble/setup.bash
Line120:source ~/ros2_ws/install/setup.bash
Line121:source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

새 터미널
pip3 list
sudo apt install python3-pip
pip3 list | grep setuptools
pip3 install setuptools==58.2.0
터미널 끝

/ros2_ws
colcon build
colcon build --packages-select my_py_pkg

파이썬노드 생성
cd ros2_ws/src/my_py_pkg/my_py_pkg
touch my_first_node.py
(노드생성)
setup.py 설정하기
'consule_scripts': [
	"py_node(실행파일이름) = my_py_pkg(패키지이름).my_first_node(노드파일이름):main(함수이름)"
]

노드 실행 첫 번째 방법
ros2_ws/
colcon build --packages-select my_py_pkg
source ~/.bashrc
cd ~/ros2_ws/install/my_py_pkg/lib/my_py_pkg
./py_node

노드 실행 두 번째 방법
ros2_ws/
colcon build --packages-select my_py_pkg
새 터미널
source .bashrc
ros2 run my_py_pkg(패키지이름) py_node(실행파일이름)
터미널 끝

python 패키지 생성
cd ros2_ws/src/ <-👏️중요!!! 해당 폴더에 가서 실행!
ros2 pkg create [package] --build-type ament_python --dependencies rclpy [선택]
수정: package.xml , setup.py , node파일

패키지 빌드업

1. 첫 번째 방법
/ros2_ws <-👏️중요!!! 해당 폴더에 가서 실행!
colcon build --packages-select [package]

/ros2_ws/install
. local_setup.bash

2. 두 번째 방법

/ros2_ws <-👏️ 중요!!! 해당 폴더에 가서 실행!
colcon build --packages-select [package] --symlink-install

/ 새 터미널 /cd
source .bashrc


ros2 도구들
rcl: Ros Client Library ex. rclpy, rclcpp
ros2 node list: 실행되는 node 목록을 보여준다.
ros2 node lnfo /(node이름): 실행되는 node 정보를 보여준다.
같은 node이름을 가진 복수의 node를 실행하지 말자.
rqt:  ROS는 로봇으로부터 얻을 수 있는 데이터를 쉽게 확인하고 관리할 수 있도록 rqt라고 하는 모니터링 도구를 제공합니다. rqt는 GUI 개발에 쓰이는 Qt framework 기반의 ROS software framework입니다. rqt는 우리가 지금까지 노드간 관계를 확인할 때 써 오던 rqt_graph와 같은 GUI 플러그인을 여러 개 포함하고 있습니다.
ros2 topic list: 실행되는 topic 목록을 보여준다.
ros2 topic echo /(topic이름) 실행되는 topic을 보여준다.


토픽

publisher는 자신이 topic을 publish하는 것만 알고 subscriber는 자신이 subscribe하는 것만 알고 있다.
토픽은 publisher와 subscriber 둘 다 같은 message 타입을 사용해야 한다.

1. Publisehr 생성
/ros2_ws/src/my_py_pkg/my_py_pkg
touch robot_news_station.py
chmod +x robot_news_station.py     : robot_news_station에 실행권한을 준다.
[robot_news_station 수정, setup.py 수정, package.xml 수정]
새로운 파일을 더했으니 symlink한다.
/ros2_ws
colcon build --packages-select my_py_pkg --symlink-install
새 터미널
source ~/.bashrc
터미널 끝

2. Subscriber 생성
/ros2_ws/src/my_py_pkg/my_py_pkg
touch smartphone.py
chmod +x smartphone.py
