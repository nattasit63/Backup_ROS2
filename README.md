# Backup_ROS2
My Backup code and file for ROS2 project (during my internship at COXSYS Robotics and Advanced Robotic project)

Significant Packages :

         - turtle_gazebo : Launch gazebo via launch.py , Spawn robots model in gazebo world , Twist tele_op key to move robots
                           ,Subscribe and Publish twist to another robot model to copy the first one and Publish movement to turtlesim too
                           # ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/robot1/cmd_vel
                            
