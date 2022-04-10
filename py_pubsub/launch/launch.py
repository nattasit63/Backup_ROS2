from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            namespace= "turtlesim1", package='turtlesim', executable='turtlesim_node', output='screen'),
        Node(
            namespace= "turtlesim1", package='turtlesim', executable='draw_square', output='screen'),
        # Node(
        #     package='py_pubsub', executable='talker', output='screen'),
        # Node(
        #     package='py_pubsub', executable='listener', output='screen'),
    ])