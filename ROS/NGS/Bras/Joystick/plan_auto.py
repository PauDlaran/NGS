import rospy
from sensor_msgs.msg import JointState
from moveit_msgs.msg import DisplayTrajectory
from control_msgs.msg import FollowJointTrajectoryActionResult
from moveit_msgs.msg import MoveGroupActionResult
import time

class plan_auto:
    def __init__(self):
        #Subscribers
        self.joint_states_topic = rospy.Subscriber('/move_group/fake_controller_joint_states', JointState, self.joint_states_callback)
        # self.planned_path_topic = rospy.Subscriber('/move_group/display_planned_path', DisplayTrajectory, self.planned_path_callback)
        # self.execute_trajectory_result_topic = rospy.Subscriber('/execute_trajectory/result', FollowJointTrajectoryActionResult, self.execute_trajectory_callback)
        self.move_groiup_result_topic = rospy.Subscriber('/move_group/result', MoveGroupActionResult, self.move_group_callback)
        self.mouvement_en_cours = False
        self.mouvement_completed = False
        self.joint_state_position = []

    def move_group_callback(self, data):
        # Fonction de rappel pour '/move_group/result'
        if data.error_code.val == 1:
            self.mouvement_en_cours = False
            self.mouvement_completed = True

            print("Move Group successful")
        else:
            self.mouvement_en_cours = False
            
            print("Move Group failed with error code:", data.error_code.val)


    def joint_states_callback(self, data):
        # Fonction de rappel pour '/move_group/fake_controller_joint_states'
        self.joint_positions = data.position

    # def planned_path_callback(self, data):
    #     # Fonction de rappel pour '/move_group/display_planned_path'
    #     self.planned_path = data.trajectory[0].joint_trajectory
    
    #     print("Planned Joint Positions:", self.planned_path.points)
    #     print("Duration of the trajectory:", self.planned_path.points[-1].time_from_start.to_sec())

    # def execute_trajectory_callback(self, data):
    #     # Fonction de rappel pour '/execute_trajectory/result'
    #     if data.error_code == 0:
    #         print("Trajectory execution successful")
    #     else:
    #         print("Trajectory execution failed with error code:", data.error_code)
        
    def rec_auto_plan(self):
        i = 0
        while self.mouvement_en_cours:
            self.joint_state_position[i] = self.joint_positions
            i += 1
            time.sleep(0.1)
        
        if self.mouvement_completed:
            self.mouvement_completed = False
            return self.joint_state_position
        else:
            return False
        

