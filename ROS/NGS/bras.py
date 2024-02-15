import rospy 
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose


g = MoveGroupCommander("leo_arm")

rospy.init_node("bras_control")
pose = Pose()
pose.position.x = g.get_current_pose().pose.position.x
pose.position.y = g.get_current_pose().pose.position.y
pose.position.z = g.get_current_pose().pose.position.z
pose.orientation = g.get_current_pose().pose.orientation

pose.position.x += 0.2
# pose.position.y += 0.01

joint_values = g.get_current_joint_values()

joint_values[0] += 0.2



print(g.get_current_pose())
print(g.get_current_joint_values())
# print(pose)

# g.set_goal_tolerance(0.01)
# g.set_planner_id("geometric::RRTstar")
# g.set_planning_time(10) 

g.set_pose_target(pose)
g.set_joint_value_target(joint_values)

#Pronlème: n'arrive pas à enchainer les mouvements quand on vient modifier la valeur coup sur coup
# #Tester avec des x,y,z dif, avec un programme qui prend d'autres actions, chercher sur internet, demander à luezi s'il a eu se problème
# success = g.go(wait=False)
# if not success:
#     print("Failed to plan a trajectory.")
#     print(g.get_planning_time())
# print(pose)
# print(success)

#GPT
plan_success, plan, planning_time, error_code = g.plan()

print(plan_success)
print(plan)
print(planning_time)
print(error_code)
# #GPT

g.stop()

g.clear_pose_targets()