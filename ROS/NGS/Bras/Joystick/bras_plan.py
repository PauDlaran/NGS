import rospy
import time
import copy
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose



class TeleopNode:

    def __init__(self):
        #Création du noeud ROS
        rospy.init_node("joystickbras")
    
        #Initialisation du subscriber
        # self.joy_sub = rospy.Subscriber('/joy', Joy, self.acquisition_joy)

        #Initialisation de Moveit
        self.g = MoveGroupCommander("leo_arm")
        self.go_move = False
        self.pose = Pose()
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation = self.g.get_current_pose().pose.orientation
        self.success = False

        #Initialisation des variables de position et de rotation
        self.translation_tcp = [0, 0, 0]
        self.rotation_tcp = [0, 0, 0]
        self.joints_values = self.g.get_current_joint_values()

        #Initialisation du pas de déplacement
        self.pas = 0.01
        self.pasA = 0.1


    def plan_cartesian_path(self, scale=1):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        move_group = self.g

        ## BEGIN_SUB_TUTORIAL plan_cartesian_path
        ##
        ## Cartesian Paths
        ## ^^^^^^^^^^^^^^^
        ## You can plan a Cartesian path directly by specifying a list of waypoints
        ## for the end-effector to go through. If executing  interactively in a
        ## Python shell, set scale = 1.0.
        ##
        waypoints = []

        wpose = move_group.get_current_pose().pose
        wpose.position.z -= scale * 0.1  # First move up (z)
        # wpose.position.y += scale * 0.2  # and sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.z += scale * 0.1  # Third move sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        # We want the Cartesian path to be interpolated at a resolution of 1 cm
        # which is why we will specify 0.01 as the eef_step in Cartesian
        # translation.  We will disable the jump threshold by setting it to 0.0,
        # ignoring the check for infeasible jumps in joint space, which is sufficient
        # for this tutorial.
        (plan, fraction) = move_group.compute_cartesian_path(
            waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
        )  # jump_threshold

        # Note: We are just planning, not asking move_group to actually move the robot yet:
        return plan, fraction

        ## END_SUB_TUTORIAL

    def execute_plan(self, plan):
        # Copy class variables to local variables to make the web tutorials more clear.
        # In practice, you should use the class variables directly unless you have a good
        # reason not to.
        move_group = self.g

        ## BEGIN_SUB_TUTORIAL execute_plan
        ##
        ## Executing a Plan
        ## ^^^^^^^^^^^^^^^^
        ## Use execute if you would like the robot to follow
        ## the plan that has already been computed:
        move_group.execute(plan, wait=True)

        ## **Note:** The robot's current joint state must be within some tolerance of the
        ## first waypoint in the `RobotTrajectory`_ or ``execute()`` will fail
        ## END_SUB_TUTORIAL

if __name__=='__main__':
    node = TeleopNode()
    while True:
        time.sleep(0.1)
        plan, fraction = node.plan_cartesian_path(1)
        print(plan)
        print(fraction)
        node.execute_plan(plan)
    # node.acquisition_joy
        
        
    rospy.spin()