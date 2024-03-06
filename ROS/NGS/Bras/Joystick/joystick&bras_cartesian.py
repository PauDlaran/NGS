""" 
Code principale du groupe NGS

Description: Noeud ROS permettant de contrôler le bras robotique LEO avec un joystick selon de manières
    - Déplacement en coordonnées cartésiennes et joints pour les rotations
    - Déplacement automatique vers des points prédéfinis

Pub : 
   - /com_arduino (std_msgs/String) : Envoi des données de position des axes du bras à l'arduino
Sub :
   - /joy (sensor_msgs/Joy) : Acquisition des données du joystick

Projet Fil Rouge, Sysm@p | Groupe NGS 
Paul Daran MKX07
Fev 2024
"""

import rospy
import math
import time
import copy
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander
from geometry_msgs.msg import Pose
from sensor_msgs.msg import JointState
from moveit_msgs.msg import MoveGroupActionResult

import plan_auto

class TeleopNode:

    def __init__(self):
        #Création du noeud ROS
        rospy.init_node("joystickbras")
    
        #Initialisation du subscriber
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.acquisition_joy) #Queue size = 1 ??
        self.joint_sate_sub = rospy.Subscriber('/move_group/fake_controller_joint_states', JointState, self.chose_pose_to_plan)
        self.move_group_result_sub = rospy.Subscriber('/move_group/result', MoveGroupActionResult, self.move_group_callback)

        #Initialisation du publisher
        self.pub = rospy.Publisher('/com_arduino', String, queue_size=10)
        self.rate = rospy.Rate(0.5)

        #####Initialisation de Moveit
        #Group
        self.g = MoveGroupCommander("pipoudou_arm")
        self.h = MoveGroupCommander("pipoudou_hand")

        #Initial poses
        self.pose = Pose()
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation = self.g.get_current_pose().pose.orientation
    
        #Initial joints
        self.joints_values_axe1 = self.g.get_current_joint_values()[0]
        self.joints_values_axe4 = self.g.get_current_joint_values()[3]

        self.joint_values_pince_main = self.h.get_current_joint_values()[0]
        self.joint_values_pince_doigt1 = self.h.get_current_joint_values()[1]
        self.joint_values_pince_doigt2 = self.h.get_current_joint_values()[2]
        self.joint_values_pince_doigt3 = self.h.get_current_joint_values()[3]

        ####Position préenregistrée (joints values [rad])
        # Initialisation de position pince
        self.joint_pince_fermee = [0, 0.4488, 0, -0.4764]
        self.joint_pince_ouverte = [1.0472, 0.4488, 1.0472, 0.5672]

        #Position Reel, prise sur le bras 
        self.ptn_pass = [0.15, 0.4754, -1.3467, 0.135]
        self.ptn_passboite1 = [1.214, 0.5035, -1.2975, -0.4747]
        self.ptn_passboite2 = [1.8162, 0.6758, -1.5117, -0.4747]
        self.ptn_passboite3 = [2.4103, 0.5108, -1.2862, -0.4747]

        self.ptn_frottiHaut_bras = [1.8113, 0.6581, -1.2479, -0.3324]
        self.ptn_frottiHaut_axe5 = 1.0084

        self.ptn_frottiBas_bras = [1.8113, 0.6581, -0.8969, -0.0856]
        self.ptn_frottiBas_axe5 = 1.0084

        self.joint_operationel = [-1.555, 0.6924, -0.9283, -0.2161]
        
        self.ptn_sortiepark = [-3.1515, -0.0307, -0.3040, -0.20605]
        self.ptn_sortiepark_axe5 = -0.9709

        self.joint_parking = [-3.15, 0.0, 0.0, 0.0]

        #Variable pour connaitre l'axe à déplacer
        self.success = False
        self.planr = False
        self.planz = False
        self.axe1 = False
        self.plan_axe4 = False
        self.planPince_doigts = False
        self.planPince_main = False

        self.planAuto = False
        self.displacement = 0

        self.auto_pose = 0

        #Initialisation de la position du bras en POLAIRE
        self.r, self.theta = self.calcul_r_theta(self.pose.position.x, self.pose.position.y)

        #Initialisation du pas de déplacement
        self.pas = 0.005
        self.pasA= 0.001 #r

        #REC 
        self.REC_success_plan = 0
        self.REC_joint_position = [0]

    #CODE FONCTIONNEL
    #region
    #Init de toutes les positions pour éviter les problèmes lors de changements de type de coordonnées
    def initialisation_pose(self):
        self.pose.position.x = self.g.get_current_pose().pose.position.x
        self.pose.position.y = self.g.get_current_pose().pose.position.y
        self.pose.position.z = self.g.get_current_pose().pose.position.z
        self.pose.orientation.x = self.g.get_current_pose().pose.orientation.x
        self.pose.orientation.y = self.g.get_current_pose().pose.orientation.y
        self.pose.orientation.z = self.g.get_current_pose().pose.orientation.z
        self.pose.orientation.w = self.g.get_current_pose().pose.orientation.w

    def initialisation_joint(self):
        self.joints_values_axe1 = self.g.get_current_joint_values()[0]
        self.joints_values_axe4 = self.g.get_current_joint_values()[3]
        self.joint_values_pince_main = self.h.get_current_joint_values()[0]
        self.joint_values_pince_doigt1 = self.h.get_current_joint_values()[1]
        self.joint_values_pince_doigt2 = self.h.get_current_joint_values()[2]
        self.joint_values_pince_doigt3 = self.h.get_current_joint_values()[3]

    def initialisation_r_theta(self):
        self.r, self.theta = self.calcul_r_theta(self.g.get_current_pose().pose.position.x, self.g.get_current_pose().pose.position.y)
   
    #Acquisition et traitement des données du joystick
    def acquisition_joy(self, joy_msg):
        #region
        # time.sleep(0.1)
        axes = joy_msg.axes
        buttons = joy_msg.buttons

        #Incrémentation pour x tcp
        if axes[1] > 0:
            self.r += self.pasA
            self.planr = True
            self.displacement = 1
        if axes[1] < 0:
            self.r -= self.pasA
            self.planr = True
            self.displacement = 1
            

        #Incrémentation pour axe1 base (y)
        if axes[0] > 0 and -3.1515 <= self.joints_values_axe1 <= 2.96706:
            self.joints_values_axe1 -= self.pas
            self.axe1 = True
            self.displacement = 2
        if axes[0] < 0 and -3.1515 <= self.joints_values_axe1 <= 2.96706:
            self.joints_values_axe1 += self.pas
            self.axe1 = True
            self.displacement = 2

        #Incrémentation pour z tcp
        if buttons[2] != 0:
            self.pose.position.z += self.pas
            self.planz = True
            self.displacement = 3
        if buttons[3] != 0:
            self.pose.position.z -= self.pas
            self.planz = True
            self.displacement = 3
        
        #Incrémentation pour angle tcp
        if axes[5] > 0 and -1.35 < self.joints_values_axe4 < 1.35:
            self.joints_values_axe4 += self.pas
            self.plan_axe4 = True
            self.displacement = 4
        if axes[5] < 0 and -1.35 < self.joints_values_axe4 < 1.35:
            self.joints_values_axe4 -= self.pas
            self.plan_axe4 = True
            self.displacement = 4

        #Incrémentation pour pince
        if buttons[0] != 0 and -0.1 < self.joint_values_pince_doigt1 < 0.9:
            self.joint_values_pince_doigt1 += self.pas
            self.joint_values_pince_doigt2 += self.pas
            self.joint_values_pince_doigt3 += self.pas
            self.planPince_doigts = True            
            self.displacement = 5
            print("pince ouverte")
        if buttons[1] != 0 and -0.1 < self.joint_values_pince_doigt1 < 0.9:
            self.joint_values_pince_doigt1 -= self.pas
            self.joint_values_pince_doigt2 -= self.pas
            self.joint_values_pince_doigt3 -= self.pas
            self.planPince_doigts = True
            self.displacement = 5
            print("pince fermée")

        if axes[4] > 0 and -1.93518 <= self.joint_values_pince_main <= 2.0944:
            self.joint_values_pince_main += self.pas
            self.planPince_main = True
            self.displacement = 6
        if axes[4] < 0:
            self.joint_values_pince_main -= self.pas
            self.planPince_main = True
            self.displacement = 6
        #endregion
        ######################################
        ## Déplacement automatique du bras ##
        ######################################
        
        # Parking +Z
        if buttons[4] != 0:
            self.auto_pose = 1
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True

        # Lambda vers opérationnel
        if buttons[9] != 0:
            self.auto_pose = 2
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True
        
        # point de passage droite
        if buttons[13] != 0:
            self.auto_pose = 3
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True

        # z boite 3
        if buttons[12] != 0:
            self.auto_pose = 4
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True

        # z boite 2
        if buttons[11] != 0:
            self.auto_pose = 5
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True

        # z boite 1
        if buttons[10] != 0:
            self.auto_pose = 6
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True

        # z frotti
        if buttons[14] != 0:
            self.auto_pose = 7
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True

    ####Calculs
    #Calculs des coordonnées polaires
    def calcul_r_theta(self, x, y):
        r = math.sqrt(x**2 + y**2)
        theta = 2 * math.atan(y/(x+math.sqrt(x*x+y*y)))
        return r, theta
 
    #Calculs des coordonnées cartésiennes
    def polar_to_cartesian(self, r, theta):
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return x, y

    ####Planification
    ##BRAS
    #Plan selon l'axe du bras (r en coordonées polaire)
    def plan_cartesian_path_r(self):
        #Conversion des coordonnées polaires en cartésiennes
        self.pose.position.x, self.pose.position.y = self.polar_to_cartesian(self.r, self.theta)

        #Plan
        waypoints = []       
        waypoints.append(copy.deepcopy(self.pose))
        (plan, fraction) = self.g.compute_cartesian_path(
            waypoints, 0.02, 0.0)
        return plan
    
    #Plan selon l'axe z
    def plan_cartesian_path_z(self):
        waypoints = []
        waypoints.append(copy.deepcopy(self.pose))
        (plan, fraction) = self.g.compute_cartesian_path(
            waypoints, 0.02, 0.0)
        return plan

    #Plan selon la rotation de l'axe1 (base)
    def set_JointVal_axe1(self):
        joints = self.g.get_current_joint_values()
        joints[0] = self.joints_values_axe1
        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()

    #Plan selon la rotation de l'axe4
    def set_JointVal_axe4(self):
        joints = self.g.get_current_joint_values()
        joints[3] = self.joints_values_axe4
        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()

    ##PINCE
    #Plan des doigts de la pince (n'est en réalité qu'un moteur, mais necessaire pour la simulation)
    def set_pose_goal_pince_doigts(self):
        joints = self.h.get_current_joint_values()
        joints[1] = self.joint_values_pince_doigt1
        joints[2] = self.joint_values_pince_doigt2
        joints[3] = self.joint_values_pince_doigt3
        self.success = self.h.go(joints, wait=False)
        # time.sleep(0.2)
        self.h.stop()
        self.h.clear_pose_targets()

    #Plan pour le poignet de la pince (+/- 120°)
    def set_pose_goal_pince_main(self):
        joints = self.h.get_current_joint_values()
        joints[0] = self.joint_values_pince_main
        self.success = self.h.go(joints, wait=False)
        # time.sleep(0.2)
        self.h.stop()
        self.h.clear_pose_targets()

    #Donne à l'arduino les données de position des axes en brut de moveit (radian), la conversion se fait dans la RPi
    def send_to_arduino(self):
        self.joints_values_pub = self.g.get_current_joint_values(), self.h.get_current_joint_values()
        print("Tram_arduino_classic")
        self.pub.publish(str(self.joints_values_pub))

    #Exécution du plan selon la position du TCP (carthésien)
    def execute_plan(self, plan):
        self.g.execute(plan, wait=False)

    #endregion

    #Fonction de rappel pour '/move_group/result'
    def move_group_callback(self, data):
        self.REC_success_plan = data.result.error_code.val #Si ==1, alors plannification réussie
        self.REC_joint_position = data.result.planned_trajectory.joint_trajectory.points #Position des joints
        print("longueur joint : ")
        print(len(self.REC_joint_position))
    
    #Tentative de planification auto, grâce à des points prédéfinies (parking, opérationnel, ...)
    def chose_pose_to_plan(self, autopose):
        joints = self.g.get_current_joint_values()

        ####Réalise le déplacement dans la simu selon le point choisi
        #Z au dessus de parcking
        if autopose == 1:            
            joints =  self.ptn_sortiepark

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()

        #Opérationnel
        if autopose == 2:
            joints = self.joint_operationel

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Pnt de passage droite
        if autopose == 3:
            joints = self.ptn_pass
            
            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Z boite 3
        if autopose == 4:
            joints = self.ptn_passboite3

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Z boite 2
        if autopose == 5:
            joints = self.ptn_passboite2

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Z boite 1
        if autopose == 6:
            joints = self.ptn_passboite1

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Z frotti (boite 2)
        if autopose == 7:
            joints = self.ptn_frottiHaut_bras

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()



if __name__=='__main__':
    node = TeleopNode()
    displacement = node.displacement

    while True:
        if displacement != node.displacement:
            node.initialisation_joint()
            node.initialisation_pose()
            node.initialisation_r_theta()

        time.sleep(0.1)
        node.acquisition_joy
        
        #Controle position pré-enregistrée, envoi à l'arduino
        if node.planAuto:
            print("Auto")
            #Envoi les coordonées des joints à l'arduino avec les données enregistrés si réussite du déplacement
            # if node.REC_success_plan == 1 and node.planAuto:
            local_REC_joint_position = node.REC_joint_position
            for i in range(len(local_REC_joint_position)):
                # print("tram REC :")
                # print(node.REC_joint_position[i].positions)
                # print(i)
                pub = local_REC_joint_position[i].positions, node.h.get_current_joint_values()
                node.pub.publish(str(pub))
                # node.rate.sleep()
                time.sleep(2)
            # else:
            #     print("P")

            node.REC_success_plan = 0
            node.REC_joint_position = []
            node.planAuto = False
        

        #Controle Joystick
        if node.planz:
            node.execute_plan(node.plan_cartesian_path_z())
            node.send_to_arduino()
            node.planz = False
            
        if node.planr:
            node.execute_plan(node.plan_cartesian_path_r())
            node.send_to_arduino()
            node.planr = False
            
        if node.axe1:
            node.set_JointVal_axe1()
            node.send_to_arduino()
            node.axe1 = False
        
        if node.plan_axe4:
            node.set_JointVal_axe4()
            node.send_to_arduino()
            node.plan_axe4 = False
        
        if node.planPince_doigts:
            node.set_pose_goal_pince_doigts()
            node.send_to_arduino()
            node.planPince_doigts = False
        
        if node.planPince_main:
            node.set_pose_goal_pince_main()
            node.send_to_arduino()
            node.planPince_main = False
        
        time.sleep(1)

        displacement = node.displacement
        time.sleep(0.1)
        # print("------\n",node.pose)
        
    rospy.spin()