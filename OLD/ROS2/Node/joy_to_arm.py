# Node sous ROS2 pour venir lire sur le topic joy_node les entrées d'une manette, réaliser un traitement grace à une matrice d'état qui décrit la position du TCP, matrice d'état qui est publié et interprété par Moveit2
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy

class JoytoArm(Node):

    def __init__(self):
        super().__init__('JoytoArm')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
        
        axe_values = msg.axes
        button_values = msg.buttons

        self.get_logger().info('Valeurs des axes: "%s"' % axe_values)
        self.get_logger().info('Valeurs des boutons: "%s"' % button_values)
        