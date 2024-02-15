import rospy
from sensor_msgs.msg import Joy

class TeleopNode:

    def __init__(self):
        rospy.init_node("joystick_test")
        joy_sub = rospy.Subscriber('/joy', Joy, self.acquisition_joy)

        self.translation_tcp = [0, 0, 0]
        self.rotation_tcp = [0, 0, 0]

        self.pas = 0.1

    def acquisition_joy(self, joy_msg):

        axes = joy_msg.axes
        buttons = joy_msg.buttons
        # rospy.loginfo(joy_msg.axes)
        # rospy.loginfo(joy_msg.buttons)

        #Incrémentation pour x tcp
        if axes[1] > 0:
            self.translation_tcp[0] = self.translation_tcp[0] + self.pas
            print("x = ", self.translation_tcp[0])
        if axes[1] < 0:
            self.translation_tcp[0] = self.translation_tcp[0] - self.pas
            print("x = ", self.translation_tcp[0])

        #Incrémentation pour y tcp
        if axes[0] > 0:
            self.translation_tcp[1] = self.translation_tcp[1] - self.pas
            print("y = ", self.translation_tcp[1])
        if axes[0] < 0:
            self.translation_tcp[1] = self.translation_tcp[1] + self.pas
            print("y = ", self.translation_tcp[1])

        #Incrémentation pour z tcp
        if buttons[2] != 0:
            self.translation_tcp[2] = self.translation_tcp[2] + self.pas
            print("z = ", self.translation_tcp[2])
        if buttons[3] != 0:
            self.translation_tcp[2] = self.translation_tcp[2] - self.pas
            print("z = ", self.translation_tcp[2])
        
        def 


        
if __name__=='__main__':
    node = TeleopNode()
    while True:
        node.acquisition_joy
    rospy.spin()