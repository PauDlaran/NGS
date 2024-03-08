import rospy
import time
import copy

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Pose
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander

class test_control:

    def __init__(self):
        rospy.init_node('test_control')

        self.joy_sub = rospy.Subscriber('/joy', Joy, self.joy_callback)

        self.move_group = MoveGroupCommander('leo_arm')

        self.pose = Pose()
        self.pose.position.x = self.move_group.get_current_pose().pose.position.x
        self.pose.position.y = self.move_group.get_current_pose().pose.position.y
        self.pose.position.z = self.move_group.get_current_pose().pose.position.z
        self.pose.orientation.x = self.move_group.get_current_pose().pose.orientation.x

        self.joints_values = self.move_group.get_current_joint_values()

        self.planCart = False
        self.planJoint = False

        self.pas = 0.001

    def joy_callback(self, joy_msg):
        axes = joy_msg.axes
        buttons = joy_msg.buttons

        while True:
            if axes[1] > 0:
                self.pose.position.x += self.pas
                planCart = True
            if axes[1] < 0:
                self.pose.position.x -= self.pas
                planCart = True
            
            if axes[0] > 0:
                self.pose.position.y += self.pas
                planCart = True
            if axes[0] < 0:
                self.pose.position.y -= self.pas
                planCart = True

            if buttons[2] != 0:
                self.pose.position.z += self.pas
                planCart = True
            if buttons[3] != 0:
                self.pose.position.z -= self.pas
                planCart = True

    def plan_cartesian(self):
        waypoints = []
        waypoints.append(copy.deepcopy(self.pose))

        plan, fraction = self.move_group.compute_cartesian_path(waypoints, 0.01, 0.0)

        return plan
    
    def plan_joint(self):
        self.move_group.set_joint_value_target(self.joints_values)
        

    def main(self):
        while True:
            self.joy_callback
            if self.planCart:
                plan = self.plan_cartesian()
                self.move_group.execute(plan)
                self.planCart = False
            if self.planJoint:
                self.plan_joint()
                self.move_group.go()
                self.planJoint = False
            time.sleep(0.1)
            print("boucle")

if __name__ == '__main__':
    test = test_control()
    test.main()