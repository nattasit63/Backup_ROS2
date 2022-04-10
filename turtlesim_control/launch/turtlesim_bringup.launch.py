from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node


def generate_launch_description():

    # args that can be set from the command line or a default will be used
    gain_arg = DeclareLaunchArgument(
        "gain", default_value=TextSubstitution(text="3.0")
    )
    
    # start a turtlesim_node in the turtlesim1 namespace
    turtlesim_node = Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        )

    # start another turtlesim_node in the turtlesim2 namespace
    # and use args to set parameters
    turtlesim_controller = Node(
            package='turtlesim_control',
            executable='controller',
            name='control',
            parameters=[{
                "linear_gain": LaunchConfiguration('gain'),
            }],
            remappings=[
                ('/pose', '/turtle1/pose'),
                ('/cmd_vel', '/turtle1/cmd_vel'),
            ]
        )

    turtlesim_scheduler = Node(
            package='turtlesim_control',
            executable='scheduler',
            remappings=[
                ('/pose', '/turtle1/pose'),
            ]
        )
    return LaunchDescription([
        gain_arg,
        turtlesim_node,
        turtlesim_controller,
        turtlesim_scheduler,
    ])