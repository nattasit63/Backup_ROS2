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
    pkg_dir = get_package_share_directory('turtle_gazebo')
    world_file_name = 'nothing.world'
    world = os.path.join(pkg_dir, 'world', world_file_name)

    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(pkg_dir, 'urdf')
    robot_description_path =  os.path.join(pkg_dir,"urdf","model.sdf",)
    robot_description = {"robot_description": xacro.process_file(robot_description_path).toxml()}
    
    launch_file_dir = os.path.join(pkg_dir, 'launch')

    
 
    gazebo = ExecuteProcess(cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],output='screen')
    spawn_entity = Node(package='turtle_gazebo', executable='spawn_turtle',arguments=['robot1', 'robot1', '1', '0', '0.0'],output='screen')
    spawn_entity2 = Node(package='turtle_gazebo', executable='spawn_turtle',arguments=['robot2', 'robot2', '0', '0', '0.0'], output='screen')
    turtlesim_node = Node(package='turtlesim',executable='turtlesim_node',name='sim')
    follow_first_robot = Node(package='turtle_gazebo',executable='follow_first_robot',name='follow_robot')
    
    return LaunchDescription([
        gazebo,
        spawn_entity,
        spawn_entity2,
        #follow_first_robot,
        #turtlesim_node,
    ])



