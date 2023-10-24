import rospy
from sensor_msgs.msg import Joy
from moveit_commander import MoveGroupCommander

axes = [0]*8
buttons = [0]*11
class TeleopNode:
    def __init__(self):
        rospy.init_node('teleop_node')
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        #self.arm = MoveGroupCommander('arm_group')
        #self.arm.set_max_velocity_scaling_factor(0.1)

    def joy_callback(self, joy_msg):
        # Map joystick inputs to arm movements
        # ...
        global axes, buttons
        axes = [round(value,3) for value in joy_msg.axes]
        buttons = joy_msg.buttons
        
        a0 = axes[0]
        a1 = axes[1]
        a2 = axes[2]
        a3 = axes[3]
        a4 = axes[4]
        a5 = axes[5]
        # Publish arm movement commands
        rospy.loginfo("\n")
        rospy.loginfo("avancer/reculer: %s", a0)
        rospy.loginfo("\n")
        #self.arm.set_joint_value_target(joint_positions)
        #self.arm.go()

if __name__ == '__main__':
    node = TeleopNode()
    rospy.spin()
