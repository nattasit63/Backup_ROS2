import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np
import math

from std_srvs.srv import Empty


class Turtlefollow(Node):

    def __init__(self):
        super().__init__('turtlefollow')
        self.publisher = self.create_publisher(Twist,'/turtle2/cmd_vel',10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period,self.timer_callback)
        self.init_time = self.get_clock().now()
        self.goal = np.array([0,0])
        self.pose2 = np.array([0,0])
        self.pose = np.array([0,0])
        self.current_position = np.array([0,0])
        self.current_position2 = np.array([0,0])
        self.current_orientation = 0.0
        self.current_orientation2 = 0.0
        self.dp = np.array([0,0])
        self.cmd_vel_msg = Twist()
        self.k_v =  1.0
        self.k_w = 1.0
    def pose_callback(self,msg):
        self.pose[0] = msg.x
        self.pose[1] = msg.y
        self.current_orientation  = msg.theta
    def pose_callback2(self,msg):
        self.pose2[0] = msg.x
        self.pose2[1] = msg.y
        self.current_orientation2  = msg.theta
    
    def timer_callback(self):
            self.subscription = self.create_subscription(Pose,'/turtle1/pose',self.pose_callback,10)
            self.subscription2 = self.create_subscription(Pose,'/turtle2/pose',self.pose_callback2,10)
            self.goal[0] = self.pose[0]
            self.goal[1] = self.pose[1]
            dp = [self.goal[0]-self.pose2[0],self.goal[1]-self.pose2[1]]
            dist = np.linalg.norm(dp)
            msg = Twist()
            if dist >0.5:
                v,w = self.control()
                msg.linear.x = v
      
                msg.angular.z = w
                self.publisher.publish(msg)
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
                self.publisher.publish(msg)
    def follow(self):
        self.subscription = self.create_subscription(Pose,'/turtle1/pose',self.pose_callback,10)
        self.subscription2 = self.create_subscription(Pose,'/turtle2/pose',self.pose_callback2,10)
        self.goal[0] = self.pose[0]
        self.goal[1] = self.pose[1]
    def publish_cmd(self):
        self.dp[0] = self.goal[0] - self.pose2[0]
        v,w = self.control()
        self.cmd_vel_msg.linear.x =v
        self.cmd_vel_msg.angular.z = w
        self.publisher.publish(self.cmd_vel_msg)

    def control(self):
        self.dp[0] = self.goal[0] - self.pose2[0]
        self.dp[1] = self.goal[1] - self.pose2[1]
        v = self.k_v
        if np.linalg.norm(self.dp)< 0.5:
            v = 0.0
        e = math.atan2(self.dp[1],self.dp[0])-self.current_orientation2
        w = self.k_w*math.atan2(math.sin(e),math.cos(e)) 
        return v,w

def main(args=None):
    rclpy.init(args=args)
    turtlefollow = Turtlefollow()
    rclpy.spin(turtlefollow)
    turtlefollow.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()