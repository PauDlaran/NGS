import rospy
from sensor_msgs.msg import JointState
from moveit_msgs.msg import DisplayTrajectory
from control_msgs.msg import FollowJointTrajectoryActionResult
from moveit_msgs.msg import MoveGroupActionResult
from geometry_msgs.msg import Pose
import time
import copy
from moveit_commander import MoveGroupCommander

class plan_auto:
    def __init__(self):
        rospy.init_node('plan_auto_test', anonymous=True)

        #Subscribers
        self.joint_states_topic = rospy.Subscriber('/move_group/fake_controller_joint_states', JointState, self.joint_states_callback)
        self.move_group_result_topic = rospy.Subscriber('/move_group/result', MoveGroupActionResult, self.move_group_callback)
        self.mouvement_en_cours = False
        self.mouvement_completed = False
        self.joint_state_position = []

        self.g = MoveGroupCommander("pipoudou_arm")

        self.joint_operationel = [-1.555, 0.6924, -0.9283, -0.2161]
        self.joint_droit = [-1.5691, 0.9206, -2.7592, -0.2618]


    def move_group_callback(self, data):
        # Fonction de rappel pour '/move_group/result'
        # print(data)
        # print(data.result.planned_trajectory.joint_trajectory.points[0].positions)
        print("nombre de frames: ")
        print(len(data.result.planned_trajectory.joint_trajectory.points))
        print("position des joints: ")
        print(data.result.planned_trajectory.joint_trajectory.points[0].positions)
        print(data.result.planned_trajectory.joint_trajectory.points[1].positions)
        print(data.result.planned_trajectory.joint_trajectory.points[2].positions)
        print(data.result.planned_trajectory.joint_trajectory.points[3].positions)
        print(data.result.planned_trajectory.joint_trajectory.points[4].positions)

        if data.result.error_code.val == 1:
            self.mouvement_en_cours = False
            self.mouvement_completed = True

            print("Move Group successful")
        else:
            self.mouvement_en_cours = False

            print("Move Group failed with error code:", data.error_code.val)

    def joint_states_callback(self, data):
        # Fonction de rappel pour '/move_group/fake_controller_joint_states'
        self.joint_positions = data.position

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

    def set_joint_goal(self):
        # joints = self.g.get_current_joint_values()
        joints = self.joint_operationel
        # joints = self.joint_droit

        self.success = self.g.go(joints, wait=True)
        # time.sleep(0.2)

        self.g.stop()
        self.g.clear_pose_targets()



if __name__ == '__main__':
    plan = plan_auto()

    plan.set_joint_goal()

    result = plan.rec_auto_plan()
    print(result)

    rospy.spin()

