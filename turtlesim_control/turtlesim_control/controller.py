from turtle import goto
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import numpy as np
import math
from turtlesim_control_srv.srv import SetGoal, SetGain, GetGain
from std_srvs.srv import Empty


class TurtlesimController(Node):
    def __init__(self):
        super().__init__('turtlesim_controller')
        self.publisher = self.create_publisher(Twist,'cmd_vel',10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period,self.timer_callback)
        self.init_time = self.get_clock().now()
        self.subscription = self.create_subscription(Pose,'pose',self.pose_callback,10)
        self.pose = Pose()
        self.subscription
        self.service_goal = self.create_service(SetGoal,'controller/set_goal',self.set_goal_callback)
        self.service_get_gain = self.create_service(GetGain,'controller/get_gain',self.get_gain_callback)
        self.service_set_gain = self.create_service(SetGain,'controller/set_gain',self.set_gain_callback)
        self.service_enable_control = self.create_service(Empty,'controller/enable',self.en_control_callback)
        self.service_disable_control = self.create_service(Empty,'controller/disable',self.dis_control_callback)

        self.client_notify_arrival = self.create_client(Empty,'scheduler/notify_arrival')
        
        while not self.client_notify_arrival.wait_for_service(timeout_sec=1):
            self.get_logger().info('service not available, waiting again...')
        self.request_notify_arrival = Empty.Request()
        self.declare_parameter('linear_gain',1.0)
        self.goal = np.array([2.0,3.0])
        self.k_v = self.get_parameter('linear_gain').value
        self.k_w = 10.0
        self.mode = 0
    def pose_callback(self,msg):
        self.pose = msg
    def send_request_notify_arrival(self):
        self.future = self.client_notify_arrival.call_async(self.request_notify_arrival)
    def timer_callback(self):
        if self.mode == 1:
            dp = self.goal-np.array([self.pose.x,self.pose.y])
            dist = np.linalg.norm(dp)
            msg = Twist()
            if dist >0.2:
                v,w = self.control(self.goal)
                msg.linear.x = v
                msg.angular.z = w
                self.publisher.publish(msg)
            else:
                msg.linear.x = 0.0
                msg.angular.z = 0.0
                self.mode = 0
                self.publisher.publish(msg)
                self.send_request_notify_arrival()
                self.get_logger().info('Robot is stopped.')
        
    def control(self,goal):
        dp = goal-np.array([self.pose.x,self.pose.y])
        v = self.k_v
        e = math.atan2(dp[1],dp[0])-self.pose.theta
        w = self.k_w*math.atan2(math.sin(e),math.cos(e)) 
        return v,w
    def set_goal_callback(self,request,response):
        self.goal = np.array([request.x,request.y])
        self.get_logger().info('Set Goal to : [%f,%f]' % (request.x,request.y))
        return response
    def get_gain_callback(self,request,response):
        response.k_v = self.k_v
        response.k_w = self.k_w 
        self.get_logger().info('The current gain (k_v,k_w) is : [%f,%f]' % (self.k_v,response.k_w))
        return response
    def set_gain_callback(self,request,response):
        #self.k_v = request.k_v
        self.k_w = request.k_w 
        self.get_logger().info('Set the current gain (k_v,k_w) to : [%f,%f]' % (request.k_v,request.k_w))
        return response
    def en_control_callback(self,request,response):
        self.mode = 1
        self.get_logger().info('Controller is enabled.')
        return response
    def dis_control_callback(self,request,response):
        self.mode = 0
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher.publish(msg)
        self.get_logger().info('Controller is disabled.')
        return response
def main(args=None):
    rclpy.init(args=args)
    turtlesimController = TurtlesimController()
    rclpy.spin(turtlesimController)
    turtlesimController.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
