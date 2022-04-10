from platform import node
import tf2_ros as tf
import tf2_msgs as tt
import tf_transformations 
from geometry_msgs.msg import PoseStamped, TransformStamped,Twist
from std_msgs.msg import Header
from turtlesim.msg import Pose as tPose
import numpy as np
import math
import rclpy
from rclpy.node import Node

class turtle_tf2(Node) :
    def __init__(self):
        super().__init__('tf2_broadcast')
        self.pose = tPose()
        self.pose2 = tPose()
        self.sub_pos1 = self.create_subscription(tPose,'/turtle1/pose',self.callback_current_pose,10)
        self.sub_pos2 = self.create_subscription(tPose,'/turtle2/pose',self.callback_current_pose2,10)
       # self.timer = rospy.Timer(rospy.Duration(1.0 / 10), self.tfBroadcasting)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period,self.tfBroadcasting)
        self.init_time = self.get_clock().now()

    def callback_current_pose(self,msg):
        self.pose = msg
    def callback_current_pose2(self,msg):
        self.pose2 = msg
    def tfBroadcasting(self):
        br = tf.TransformBroadcaster(Node)
        t = TransformStamped()
        h = Header()
        h.stamp = self.get_clock().now()
        h.frame_id = 'world'
        t.header = h
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.pose.x
        t.transform.translation.y = self.pose.y
        t.transform.translation.z = 0.0
        rotation = tf_transformations.euler_from_quaternion(0,0,self.pose.theta)
        t.transform.rotation.x = rotation[0]
        t.transform.rotation.y = rotation[1]
        t.transform.rotation.z = rotation[2]
        t.transform.rotation.w = rotation[3]
        br.sendTransform(t)

        # br2 = tf.TransformBroadcaster()
        # t2 = TransformStamped()
        # h2 = Header()
        # h2.stamp = self.get_clock().now()
        # h2.frame_id = 'world'
        # t2.header = h2
        # t2.child_frame_id = 'base_footprint2'
        # t2.transform.translation.x = self.pose2.x
        # t2.transform.translation.y = self.pose2.y
        # t2.transform.translation.z = 0.0
        # rotation2 = tf_transformations.euler_from_quaternion(0,0,self.pose2.theta)
        # t2.transform.rotation.x = rotation2[0]
        # t2.transform.rotation.y = rotation2[1]
        # t2.transform.rotation.z = rotation2[2]
        # t2.transform.rotation.w = rotation2[3]
        # br2.sendTransform(t2)
    
def main(args=None):
    rclpy.init(args=args)
    tf_broadcaster = turtle_tf2()
    rclpy.spin(tf_broadcaster)
    tf_broadcaster.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()