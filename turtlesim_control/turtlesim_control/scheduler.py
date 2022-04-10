import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from turtlesim.msg import Pose
import numpy as np
from turtlesim_control_srv.srv import RandomizeGoal, SetGoal
from turtlesim_control_action.action import GoToGoal
from std_srvs.srv import Empty
import time

class TurtlesimControlActionServer(Node):
    frequency = 10
    def __init__(self):
        super().__init__('turtlesim_control_action_server')
        self.action_server = ActionServer(self,GoToGoal,'go_to_goal',self.execute_callback)
        self.client_enable = self.create_client(Empty,'controller/enable')
        self.client_set_goal = self.create_client(SetGoal,'controller/set_goal')
        self.rate = self.create_rate(self.frequency)

        while not self.client_enable.wait_for_service(timeout_sec=1):
            self.get_logger().info('service not available, waiting again...')
        self.request_enable = Empty.Request()
        
        while not self.client_set_goal.wait_for_service(timeout_sec=1):
            self.get_logger().info('service not available, waiting again...')
        self.request_set_goal = SetGoal.Request()
        self.pose = Pose()
        self.hasArrived = 0
        self.goal = np.array([2.0,3.0])

    def send_request_enable(self):
        self.future = self.client_enable.call_async(self.request_enable)
        
    def send_request_set_goal(self):
        self.request_set_goal.x = self.goal[0]
        self.request_set_goal.y = self.goal[1]
        self.future = self.client_set_goal.call_async(self.request_set_goal)
    def execute_callback(self, goal_handle):
        init_time = self.get_clock().now()
        self.get_logger().info('Executing action...')
        self.goal = np.array([goal_handle.request.x,goal_handle.request.y])
        self.send_request_set_goal()        
        while not self.future.done():
            self.get_logger().info('Sending goal...')
        self.hasArrived = 0
        self.send_request_enable()
        while not self.future.done():
            self.get_logger().info('Enabling controller...')
        feedback_msg = GoToGoal.Feedback()
        while not self.hasArrived:
            dp = self.goal-np.array([self.pose.x,self.pose.y])
            dist = np.linalg.norm(dp)
            feedback_msg.distance = dist
            goal_handle.publish_feedback(feedback_msg)
            self.rate.sleep()
        dt = self.get_clock().now()-init_time
        goal_handle.succeed()
        result = GoToGoal.Result()
        result.total_time = dt.nanoseconds/1e9
        return result




class TurtlesimScheduler(Node):
    def __init__(self,actionServer):
        super().__init__('turtlesim_scheduler')
        self.subscription = self.create_subscription(Pose,'pose',self.pose_callback,10)
        self.subscription
        self.action_server = actionServer

        self.service_rand = self.create_service(RandomizeGoal,'/scheduler/rand_goal',self.randomize_goal_callback)
        self.service_rand = self.create_service(Empty,'/scheduler/notify_arrival',self.notify_arrival_callback)
        
        self.client_disable = self.create_client(Empty,'controller/disable')

        while not self.client_disable.wait_for_service(timeout_sec=1):
            self.get_logger().info('service not available, waiting again...')
        self.request_disable = Empty.Request()

        self.goal = actionServer.goal
        self.pose = Pose()
        self.hasArrived = 0

    def send_request_disable(self):
        self.future = self.client_disable.call_async(self.request_disable)
    
    def pose_callback(self,msg):
        self.pose = msg
        self.action_server.pose = msg
    
    def notify_arrival_callback(self,request,response):
        self.hasArrived = 1
        self.action_server.hasArrived = 1
        self.get_logger().info('Robot has arrived!!')
        return response
    def randomize_goal_callback(self,request,response):
        self.goal = 10*np.random.rand(2)
        response.x = self.goal[0]
        response.y = self.goal[1]
        
        self.get_logger().info('Randomizing Goal to : [%f,%f]' % (response.x,response.y))  # CHANGE
        self.action_server.send_request_set_goal()
        rclpy.spin_until_future_complete(self.action_server,self.action_server.future)
        return response

def main(args=None):
    rclpy.init(args=args)
    try:
        turtlesim_control_action_server = TurtlesimControlActionServer()
        turtlesim_scheduler = TurtlesimScheduler(actionServer=turtlesim_control_action_server)
        executor = MultiThreadedExecutor(num_threads=1)
        executor.add_node(turtlesim_control_action_server)
        executor.add_node(turtlesim_scheduler)
        try:
            executor.spin()
        finally:
            executor.shutdown()
            turtlesim_scheduler.destroy_node()
            turtlesim_control_action_server.destroy_node()
    finally:
        rclpy.shutdown()
if __name__ == '__main__':
    main()
