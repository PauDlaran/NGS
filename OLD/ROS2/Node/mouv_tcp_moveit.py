import rospy
import moveit_commander
from geometry_msgs.msg import Pose

class mouvTCP:
    def __init__(self, group_name="main"):
        # Initialise le noeud ROS et le planificateur MoveIt2
        rospy.init_node('moveit2_node', anonymous=True)
        moveit_commander.roscpp_initialize(sys.argv)
        # Crée un objet MoveGroupCommander pour interagir avec le groupe de joints
        self.move_group = moveit_commander.MoveGroupCommander(group_name)

    def set_goal_position_orientation(self, position, orientation):
        # Crée un objectif de pose avec une position et une orientation spécifiées
        pose_goal = Pose()
        pose_goal.position.x = position[0]
        pose_goal.position.y = position[1]
        pose_goal.position.z = position[2]
        pose_goal.orientation.x = orientation[0]
        pose_goal.orientation.y = orientation[1]
        pose_goal.orientation.z = orientation[2]
        pose_goal.orientation.w = orientation[3]
        return pose_goal

    def plan_move_to_goal(self, pose_goal):
        # Définit l'objectif de pose pour le groupe de joints et planifie le mouvement
        self.move_group.set_pose_target(pose_goal)
        plan = self.move_group.go(wait=True)
        return plan

    def generate_trajectory(self):
        # Génère une trajectoire pour le mouvement planifié
        trajectory = self.move_group.plan()
        return trajectory

    def execute_trajectory(self, trajectory):
        # Exécute la trajectoire planifiée
        self.move_group.execute(trajectory, wait=True)

    def shutdown(self):
        # Arrête le noeud ROS et le planificateur MoveIt2
        moveit_commander.roscpp_shutdown()
        rospy.loginfo("Exiting MoveIt2 node")

if __name__ == '__main__':
    # Crée un objet mouvTCP et utilise ses méthodes pour planifier et exécuter un mouvement
    mouv = mouvTCP()
    position = [0.5, 0.0, 0.5]
    orientation = [0.0, 0.0, 0.0, 1.0]
    pose_goal = mouv.set_goal_position_orientation(position, orientation)
    plan = mouv.plan_move_to_goal(pose_goal)
    trajectory = mouv.generate_trajectory()
    mouv.execute_trajectory(trajectory)
    mouv.shutdown()