import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np
from nav_msgs.msg import Odometry

class Followrobot(Node):
    def __init__(self):
        super().__init__('followrobot')
        self.subscriber_cmd = self.create_subscription(Twist,'/robot1/cmd_vel',self.cmd1_callback,10)
        self.publisher_cmd = self.create_publisher(Twist,'/robot2/cmd_vel',10)
        self.publisher_turtle = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.subscriber_odom = self.create_subscription(Odometry,'/robot1/odom',self.odom_callback,10)
        self.publisher_odom = self.create_publisher(Odometry,'/robot2/odom',10)
        self.cmd_vel_msg_get = Twist()
        # timer_period = 0.1
        # self.timer_iter = self.create_timer(timer_period,self.subpub)

    def cmd1_callback(self,msg_twist):
        self.cmd_vel_msg_get = msg_twist
        # self.publisher_cmd.publish(self.cmd_vel_msg_get)
        # self.publisher_turtle.publish(self.cmd_vel_msg_get)
        # pass

    def odom_callback(self,msg_odom):
        self.odom = msg_odom
        self.publisher_odom.publish(msg_odom)

    # def subpub(self):
    #     self.subscriber_cmd = self.create_subscription(Twist,'/robot1/cmd_vel',self.cmd1_callback,10)
    #     # msg = Twist()
    #     # msg.linear.x = self.cmd_vel_msg_get.linear.x
    #     # msg.linear.y = self.cmd_vel_msg_get.linear.y
    #     # msg.linear.z = self.cmd_vel_msg_get.linear.z

    #     # msg.angular.x = self.cmd_vel_msg_get.angular.x
    #     # msg.angular.y = self.cmd_vel_msg_get.angular.y
    #     # msg.angular.z = self.cmd_vel_msg_get.angular.z

    #     # self.publisher_cmd.publish(msg)
    #     # self.publisher_turtle.publish(msg)
    #     self.publisher_cmd.publish(self.cmd_vel_msg_get)
    #     self.publisher_turtle.publish(self.cmd_vel_msg_get)

def main(args=None):
    rclpy.init(args=args)
    followrobot = Followrobot()
    rclpy.spin(followrobot)
    followrobot.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()

