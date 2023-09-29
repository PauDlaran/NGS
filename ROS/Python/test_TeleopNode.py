import rospy
from sensor_msgs.msg import Joy
from moveit_commander import MoveGroupCommander

axes = [0]*8
buttons = [0]*11
class TeleopNode:
    def __init__(self):
        rospy.init_node('teleop_node')
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)
        self.arm = MoveGroupCommander('arm_group')
        self.arm.set_max_velocity_scaling_factor(0.1)

    def joy_callback(self, joy_msg):
        # Map joystick inputs to arm movements
        # ...
        global axes, buttons
        axes = [round(value,3) for value in joy_msg.axes]
        buttons = joy_msg.buttons
        
        gauche_droite = axes[7]
        avancer_reculer = axes[8] 
        monter = axes[3]
        descendre = axes[6]
        A = buttons[1]
        B = buttons[2]
        X = buttons[3]
        Y = buttons[4]
        # Publish arm movement commands
        rospy.loginfo("\n")
        rospy.loginfo("gauche/droite: %s", gauche_droite)
        rospy.loginfo("avancer/reculer: %s", avancer_reculer)
        rospy.loginfo("monter: %s", monter)
        rospy.loginfo("descendre: %s", descendre)
        rospy.loginfo("A: %s", A)
        rospy.loginfo("B: %s", B)
        rospy.loginfo("X: %s", X)
        rospy.loginfo("Y: %s", Y)
        rospy.loginfo("\n")
        #self.arm.set_joint_value_target(joint_positions)
        #self.arm.go()

if __name__ == '__main__':
    node = TeleopNode()
    rospy.spin()
