from turtle import goto
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.action import ActionServer
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np
import math
from turtlesim_control_srv.srv import RandomizeGoal, SetGain, SetGoal, GetGain
from turtlesim_control_action.action import GoToGoal

class TurtlesimScheduler(Node):
    def __init__(self):
        super().__init__('turtlesim_scheduler')
        self.publisher = self.create_publisher(Twist,'cmd_vel',10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period,self.timer_callback)
        self.init_time = self.get_clock().now()
        self.subscription = self.create_subscription(Pose,'pose',self.pose_callback,10)
        self.pose = Pose()
        self.subscription
        self.service_rand = self.create_service(RandomizeGoal,'rand_goal',self.randomize_goal_callback)
        self.service_goal = self.create_service(SetGoal,'set_goal',self.set_goal_callback)
        self.service_get_gain = self.create_service(GetGain,'get_gain',self.get_gain_callback)
        self.service_set_gain = self.create_service(SetGain,'set_gain',self.set_gain_callback)
        self.declare_parameter('linear_gain',1.0)
        self.action_server = ActionServer(self,GoToGoal,'go_to_goal',self.execute_callback)
        self.goal = np.array([2.0,3.0])
        self.k_v = self.get_parameter('linear_gain').value
        self.k_w = 10.0
        self.mode = 0
    def pose_callback(self,msg):
        #self.get_logger().info('I heard: "%s"' % msg.x)
        self.pose = msg
    def timer_callback(self):   
        self.get_logger().info(str(self.mode))   
        if self.mode == 1:
            v,w = self.control(self.goal)
            msg = Twist()
            msg.linear.x = v
            msg.angular.z = w
            self.publisher.publish(msg)
            self.get_logger().info('Publishing Linear Velocity: "%s"' % msg.linear.x)
        #self.get_logger().info('Publishing Angular Velocity: "%s"' % msg.angular.z)
    def control(self,goal):
        dp = goal-np.array([self.pose.x,self.pose.y])
        v = self.k_v
        e = math.atan2(dp[1],dp[0])-self.pose.theta
        w = self.k_w*math.atan2(math.sin(e),math.cos(e)) 
        return v,w
    def randomize_goal_callback(self,request,response):
        self.goal = 10*np.random.rand(2)
        print(type(self.goal[0]))
        response.x = self.goal[0]
        response.y = self.goal[1]
        self.get_logger().info('Randomizing Goal to : [%f,%f]' % (response.x,response.y))  # CHANGE
        return response
    def set_goal_callback(self,request,response):
        self.goal = np.array([request.x,request.y])
        self.get_logger().info('Set Goal to : [%f,%f]' % (request.x,request.y))  # CHANGE
        return response
    def get_gain_callback(self,request,response):
        response.k_v = self.k_v
        response.k_w = self.k_w 
        
        self.get_logger().info('The current gain (k_v,k_w) is : [%f,%f]' % (self.k_v,response.k_w))  # CHANGE
        
        return response
    
    def set_gain_callback(self,request,response):
        #self.k_v = request.k_v
        self.k_w = request.k_w 
        self.get_logger().info('Set the current gain (k_v,k_w) to : [%f,%f]' % (request.k_v,request.k_w))  # CHANGE
        
        return response
    def execute_callback(self, goal_handle):
        self.get_logger().info(str(type(goal_handle)))
        self.get_logger().info('Executing goal...')
        feedback_msg = GoToGoal.Feedback()
        self.mode = 1
        self.goal = np.array([goal_handle.request.x,goal_handle.request.y])
        dp = self.goal-np.array([self.pose.x,self.pose.y])
        dist = np.linalg.norm(dp)

        while (dist>0.1) :
            dp = self.goal-np.array([self.pose.x,self.pose.y])
            dist = np.linalg.norm(dp)
            feedback_msg.distance = dist
        
        self.mode = 0
        msg = Twist()
        msg.linear.x = 0
        msg.angular.z = 0
        self.publisher.publish(msg)
        goal_handle.succeed()
        result = GoToGoal.Result()
        dt = self.get_clock().now()-self.init_time
        result.total_time = dt.nanoseconds/1e9
        return result
def main(args=None):
    rclpy.init(args=args)
    turtlesimController = TurtlesimController()
    rclpy.spin(turtlesimController)
    turtlesimController.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
