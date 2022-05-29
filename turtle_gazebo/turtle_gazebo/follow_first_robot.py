import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Followrobot(Node):
    def __init__(self):
        super().__init__('followrobot')
        self.subscriber_cmd = self.create_subscription(Twist,'/robot1/cmd_vel',self.cmd1_callback,10)
        self.publisher_cmd = self.create_publisher(Twist,'/robot2/cmd_vel',10)
        self.publisher_turtle = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        self.cmd_vel_msg_get = Twist()
 

    def cmd1_callback(self,msg_twist):
        self.cmd_vel_msg_get = msg_twist
        self.publisher_cmd.publish(self.cmd_vel_msg_get)
        self.publisher_turtle.publish(self.cmd_vel_msg_get)


def main(args=None):
    rclpy.init(args=args)
    followrobot = Followrobot()
    rclpy.spin(followrobot)
    followrobot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()









