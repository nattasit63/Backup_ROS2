# Backup_ROS2
My Backup code and file for ROS2 project (during my internship at COXSYS Robotics and Advanced Robotic project)

Important Packages :

         - turtle_gazebo : Launch gazebo via launch.py , Spawn robots model in gazebo world , Twist tele_op key to move robots
                           ,Subscribe and Publish twist to another robot model to copy the first one and Publish movement to turtlesim too
                           ,turtle leader-follower ,tf2 boardcastor
                           Move robot command : ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/robot1/cmd_vel
                           
         - turtlesim_control           }
           turtlesim_control_srv       }   Very Important example to do basic things in ROS2 (especially action) by Aj.PI Thanacha
           turtlesim_control_action    }
         
         - rmf_begin     : Interface(select yaml file,create node on screen) , Tutorial for Vehicle Routing Problem python
                           Do VRP (pick up and delivery) from yaml file
      
         - Others        : Tutorial to do things and Example to study
