from setuptools import setup

package_name = 'midterm'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='johs',
    maintainer_email='johs@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_speed = midterm.robot_speed:main',
            'lidar_angle = midterm.lidar_angle:main',
            'robot_window = midterm.robot_window:main'
        ],
    },
)
