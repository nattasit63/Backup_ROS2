
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir,LaunchConfiguration,FindExecutable
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import xacro
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    world_file_name = 'nothing.world'
    pkg_dir = get_package_share_directory('turtle_gazebo')

    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(pkg_dir, 'urdf')

    world = os.path.join(pkg_dir, 'world', world_file_name)
    launch_file_dir = os.path.join(pkg_dir, 'launch')
    robot_description_path =  os.path.join(pkg_dir,"urdf","model.sdf",)
    robot_description = {"robot_description": xacro.process_file(robot_description_path).toxml()}
    joint_state_publisher_node = Node(package='joint_state_publisher',executable='joint_state_publisher',name='joint_state_publisher')
    robot_state_publisher_node = Node(package="robot_state_publisher", executable="robot_state_publisher",output="both",parameters=[robot_description],)
    gazebo = ExecuteProcess(cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],output='screen')
    spawn_entity = Node(package='turtle_gazebo', executable='spawn_turtle',arguments=['robot1', 'robot1', '1', '0', '0.0'],output='screen')
    spawn_entity2 = Node(package='turtle_gazebo', executable='spawn_turtle',arguments=['robot2', 'robot2', '0', '0', '0.0'], output='screen')
    spawn_entity3 = Node(package='warehouse_robot_spawner_pkg', executable='spawn_demo',arguments=['WarehouseBot', 'ware_robot', '-1.5', '-4.0', '0.0'],output='screen')
    turtlesim_node = Node(package='turtlesim',executable='turtlesim_node',name='sim')
    spawn_turtle = ExecuteProcess(cmd=[[FindExecutable(name='ros2'),' service call ','/spawn ','turtlesim/srv/Spawn ','"{x: 2, y: 2, theta: 0}"']],shell=True)
    follow = Node(package='turtle_gazebo',executable='turtlefollow',name='follow')
    follow_first_robot = Node(package='turtle_gazebo',executable='follow_first_robot',name='follow_robot')
    
    return LaunchDescription([
        gazebo,
        spawn_entity,
        spawn_entity2,
        follow_first_robot,
        # spawn_entity3,
        # turtlesim_node,
        # spawn_turtle,
        # follow,
        # joint_state_publisher_node,
        #robot_state_publisher_node,

    ])