""" 
Code principal du groupe NGS, permet de piloter le sysm@p joint par joint avec un joystick et de l'envoyer vers de pose prédéfinie

Description: Noeud ROS permettant de contrôler le bras robotique LEO avec un joystick joint par joint

Pub : 
   - /com_arduino (std_msgs/String) : Envoi des données de position des axes du bras à l'arduino
Sub :
   - /joy (sensor_msgs/Joy) : Acquisition des données du joystick

Projet Fil Rouge, Sysm@p | Groupe NGS 
Paul Daran MKX07
Fev 2024
"""

import rospy
import time
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from moveit_commander import MoveGroupCommander
from sensor_msgs.msg import JointState
from moveit_msgs.msg import MoveGroupActionResult

class TeleopNode:

    def __init__(self):
        #Création du noeud ROS
        rospy.init_node("joystickbras")
    
        #Initialisation du subscriber
        self.joy_sub = rospy.Subscriber('/joy', Joy, self.acquisition_joy) #Queue size = 1 ??
        # self.joint_sate_sub = rospy.Subscriber('/move_group/fake_controller_joint_states', JointState, self.chose_pose_to_plan)
        self.move_group_result_sub = rospy.Subscriber('/move_group/result', MoveGroupActionResult, self.move_group_callback)

        #Initialisation du publisher
        self.pub = rospy.Publisher('/com_arduino', String, queue_size=10)


        #Initialisation de Moveit
        self.g = MoveGroupCommander("pipoudou_arm")
        self.h = MoveGroupCommander("pipoudou_hand")
        self.displacement = 0
        #Initialisation des joint
        self.joints_values_axe1 = self.g.get_current_joint_values()[0]
        self.joints_values_angle_axe2 = self.g.get_current_joint_values()[1]
        self.joints_values_angle_axe3 = self.g.get_current_joint_values()[2]
        self.joints_values_angle_axe4 = self.g.get_current_joint_values()[3]

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

        self.ptn_frotti_face = [-1.3832, 1.359, -1.002, 0.478]
        self.ptn_frotti_face_axe5 = 0.002

        self.ptn_aspi_haut = [-2.4307, 0.7403, -0.91734, 0.01899]
        self.ptn_aspi_haut_axe5 = -0.0006

        self.ptn_aspi_milieu = [-2.4288, 1.17621, -0.86753, 0.73317]
        self.ptn_aspi_milieu_axe5 = -0.0006

        self.ptn_aspi_bas = [-2.4717, 2.1211, -1.439555, 0.73585]
        self.ptn_aspi_bas_axe5 = -0.1859

        self.joint_operationel = [-1.555, 0.6924, -0.9283, -0.2161]
        
        self.ptn_sortiepark = [-3.05, -0.03, -0.18, -0.18] #PAS BONNE TODO
        self.ptn_sortiepark_axe5 = 0

        self.ptn_solide = [-0.00172, 1.54135, -1.19842, 0.449188]
        self.ptn_solide_axe5 = 0.00224

        self.joint_parking = [-3.15, 0.0, 0.0, 0.0]



        #Variable pour connaitre l'axe à déplacer
        self.axe2 = False
        self.axe3 = False
        self.axe1 = False
        self.axe4 = False
        self.planPince_doigts = False
        self.planPince_main = False

        self.z_parking = False
        self.ptn_aspi_bas_V = False
        self.ptn_aspi_milieu_V = False
        self.ptn_aspi_haut_V = False
        self.ptn_solideV = False

        self.planAuto = False
        self.displacement = 0

        

        #Initialisation du pas de déplacement
        self.pas = 0.005
        self.pasA= 0.001
        self.pasB = 0.0005

        #REC 
        self.REC_success_plan = 0
        self.positions = [0]
        self.REC_hand_joint_position = [0]
        self.run_REC_plan = False

    def initialisation_joint(self):
        #Initialisation Bras
        self.joints_values_axe1 = self.g.get_current_joint_values()[0]
        self.joints_values_angle_axe2 = self.g.get_current_joint_values()[1]
        self.joints_values_angle_axe3 = self.g.get_current_joint_values()[2]
        self.joints_values_angle_axe4 = self.g.get_current_joint_values()[3]

        #Initialisation Pince
        self.joint_values_pince_main = self.h.get_current_joint_values()[0]
        self.joint_values_pince_doigt1 = self.h.get_current_joint_values()[1]
        self.joint_values_pince_doigt2 = self.h.get_current_joint_values()[2]
        self.joint_values_pince_doigt3 = self.h.get_current_joint_values()[3]

   
    #Acquisition et traitement des données du joystick
    def acquisition_joy(self, joy_msg):
        # time.sleep(0.1)
        axes = joy_msg.axes
        buttons = joy_msg.buttons

        #region
        #Incrémentation pour rot base axe1 (y)
        if axes[0] < 0 and -3.1515 <= self.joints_values_axe1 <= 2.96706:
            self.joints_values_axe1 -= self.pasA
            self.axe1 = True
            self.displacement = 2
        if axes[0] > 0 and -3.1515 <= self.joints_values_axe1 <= 2.96706:
            self.joints_values_axe1 += self.pasA
            self.axe1 = True
            self.displacement = 2

        #Incrémentation pour rot axe2 tcp
        if axes[1] > 0:
            self.joints_values_angle_axe2 += self.pasB
            self.axe2 = True
            self.displacement = 1
        if axes[1] < 0:
            self.joints_values_angle_axe2 -= self.pasB
            self.axe2 = True
            self.displacement = 1

        #Incrémentation pour rot axe 3
        if axes[2] > 0:
            self.joints_values_angle_axe3 += self.pasA
            self.axe3 = True
            self.displacement = 3
        if axes[2] < 0:
            self.joints_values_angle_axe3 -= self.pasA
            self.axe3 = True
            self.displacement = 3
        
        #Incrémentation pour angle tcp axe4
        if axes[5] > 0 and -1.35 < self.joints_values_angle_axe4 < 1.35:
            self.joints_values_angle_axe4 += self.pas
            self.axe4 = True
            self.displacement = 4
        if axes[5] < 0 and -1.35 < self.joints_values_angle_axe4 < 1.35:
            self.joints_values_angle_axe4 -= self.pas
            self.axe4 = True
            self.displacement = 4

        #incrémentation pour rot poignet axe 5
        if axes[4] > 0 and -1.93518 <= self.joint_values_pince_main <= 2.0944:
            self.joint_values_pince_main += self.pas
            self.planPince_main = True
            self.displacement = 6
        if axes[4] < 0:
            self.joint_values_pince_main -= self.pas
            self.planPince_main = True
            self.displacement = 6

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

        
        #endregion
        
        #z parking
        if buttons[7] != 0:
            self.z_parking = True
            self.displacement = 8
        
        ##A passer en mode plan?
        #Z aspi haut 
        if buttons[5] != 0:
            self.ptn_aspi_haut_V = True
            self.displacement = 9

        #Z aspi milieu
        if buttons[4] != 0:
            self.ptn_aspi_milieu_V = True
            self.displacement = 10 
        
        #Z aspi bas
        if buttons[8] != 0:
            self.ptn_aspi_bas_V = True
            self.displacement = 11

        if buttons[14] != 0:
            self.ptn_solideV = True
            self.displacement = 12

        ######################################
        ## Déplacement automatique du bras ##
        ######################################
        

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

        #Frottis face
        if buttons[6] != 0:
            self.auto_pose = 8
            self.chose_pose_to_plan(self.auto_pose)
            self.displacement = 7
            self.planAuto = True    
        

    def set_JointVal_axe1(self):
        joints = self.g.get_current_joint_values()
        joints[0] = self.joints_values_axe1
        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()

    def set_JointVal_axe4(self):
        joints = self.g.get_current_joint_values()
        joints[3] = self.joints_values_angle_axe4
        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()
    
    def set_JointVal_axe2(self):
        joints = self.g.get_current_joint_values()
        joints[1] = self.joints_values_angle_axe2
        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()
    
    def set_JointVal_axe3(self):
        joints = self.g.get_current_joint_values()
        joints[2] = self.joints_values_angle_axe3
        self.success = self.g.go(joints, wait=False)
        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()

    def set_pose_goal_pince_doigts(self):
        joints = self.h.get_current_joint_values()
        joints[1] = self.joint_values_pince_doigt1
        joints[2] = self.joint_values_pince_doigt2
        joints[3] = self.joint_values_pince_doigt3
        self.success = self.h.go(joints, wait=False)
        # time.sleep(0.2)
        self.h.stop()
        self.h.clear_pose_targets()

    def set_pose_goal_pince_main(self):
        joints = self.h.get_current_joint_values()
        joints[0] = self.joint_values_pince_main
        self.success = self.h.go(joints, wait=False)
        # time.sleep(0.2)
        self.h.stop()
        self.h.clear_pose_targets()

    def set_z_parkingVal(self):
        joints = self.g.get_current_joint_values()
        joints = self.ptn_sortiepark
        self.success = self.g.go(joints, wait=False)

        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()
    
    def set_z_aspi_hautVal(self):
        joints = self.g.get_current_joint_values()
        joints = self.ptn_aspi_haut
        self.success = self.g.go(joints, wait=False)

        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()
    
    def set_z_aspi_milieuVal(self):
        joints = self.g.get_current_joint_values()
        joints = self.ptn_aspi_milieu
        self.success = self.g.go(joints, wait=False)

        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()
    
    def set_z_aspi_basVal(self):
        joints = self.g.get_current_joint_values()
        joints = self.ptn_aspi_bas
        self.success = self.g.go(joints, wait=False)

        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()

    def set_z_solideVal(self):
        joints = self.g.get_current_joint_values()
        joints = self.ptn_solide
        self.success = self.g.go(joints, wait=False)

        # time.sleep(0.2)
        self.g.stop()
        self.g.clear_pose_targets()
    

    #Donne à l'arduino les données de position des axes en brut de moveit, la conversion se fait dans la RPi
    def send_to_arduino(self):
        if not self.run_REC_plan:
            joints_values_pub = self.g.get_current_joint_values(), self.h.get_current_joint_values()
            self.pub.publish(str(joints_values_pub))

    def move_group_callback(self, data):
        self.REC_success_plan = data.result.error_code.val #Si ==1, alors plannification réussie
        self.REC_joint_position = data.result.planned_trajectory.joint_trajectory.points #Position des joints
        print("longueur joint : ")
        print(len(self.REC_joint_position))
    
    #Tentative de planification auto, grâce à des points prédéfinies (parking, opérationnel, ...)
    def chose_pose_to_plan(self, autopose):
        self.REC_hand_joint_position = self.h.get_current_joint_values()

        ####Réalise le déplacement dans la simu selon le point choisi
        #Z au dessus de parcking
        if autopose == 1:
            self.REC_hand_joint_position[0] = self.ptn_sortiepark_axe5

            joints = self.g.get_current_joint_values()
            joints =  self.ptn_sortiepark

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()

        #Opérationnel
        if autopose == 2:

            joints = self.g.get_current_joint_values()
            joints = self.joint_operationel

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Pnt de passage droite
        if autopose == 3:
            joints = self.g.get_current_joint_values()
            joints = self.ptn_pass
            
            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Z boite 3
        if autopose == 4:
            joints = self.g.get_current_joint_values()
            joints = self.ptn_passboite3

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Z boite 2
        if autopose == 5:
            joints = self.g.get_current_joint_values()
            joints = self.ptn_passboite2

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        
        #Z boite 1
        if autopose == 6:
            joints = self.g.get_current_joint_values()
            joints = self.ptn_passboite1

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()
        

        # Attraper le frottis devant
        if autopose == 8:
            self.REC_hand_joint_position[0] = self.ptn_frotti_face_axe5

            joints = self.g.get_current_joint_values()
            joints = self.ptn_frotti_face

            self.success = self.g.go(joints, wait=True)
            self.g.stop()
            self.g.clear_pose_targets()

if __name__=='__main__':
    node = TeleopNode()
    adisplacement = 0
    
    while True:
        
        #Initialisation des joints si changement d'axe de déplacements, permet d'éviter les faux planning
        if adisplacement != node.displacement:
            node.initialisation_joint()

            #TODO
            
        time.sleep(0.1)
        node.acquisition_joy

        if node.planAuto:
            print("Auto")
            node.run_REC_plan = True
            #Run position pince
            local_REC_hand_joint_position = node.REC_hand_joint_position
            success = node.h.go(local_REC_hand_joint_position, wait=True)
            node.h.stop()
            node.h.clear_pose_targets()

            #Envoi les coordonées des joints à l'arduino avec les données enregistrés si réussite du déplacement
            local_REC_joint_position = node.REC_joint_position
            nmbr_frame = len(local_REC_joint_position)
            if nmbr_frame % 2 != 0:
                local_REC_joint_position.append(local_REC_joint_position[-1])
                nmbr_frame +=1
            
            
            
            for i in range(0, int(nmbr_frame), 2):
                pub = local_REC_joint_position[i].positions, local_REC_hand_joint_position
                node.pub.publish(str(pub))

                time.sleep(2)

            
            node.REC_success_plan = 0
            node.REC_joint_position = []
            node.planAuto = False
            node.run_REC_plan = False

            # time.sleep(0.1)
            # node.initialisation_joint()*

        if node.z_parking:
            node.set_z_parkingVal()
            node.z_parking = False

        if node.ptn_aspi_bas_V:
            node.set_z_aspi_basVal()
            node.ptn_aspi_bas_V = False
        
        if node.ptn_aspi_milieu_V:
            node.set_z_aspi_milieuVal()
            node.ptn_aspi_milieu_V = False
        
        if node.ptn_aspi_haut_V:
            node.set_z_aspi_hautVal()
            node.ptn_aspi_haut_V = False

        if node.ptn_solideV:
            node.set_z_solideVal()
            node.ptn_solideV = False

        if node.axe1:
            node.set_JointVal_axe1()
            
            node.axe1 = False

        if node.axe2:
            node.set_JointVal_axe2()
            
            node.axe2 = False

        if node.axe3:
            node.set_JointVal_axe3()
            
            node.axe3 = False
        
        if node.axe4:
            node.set_JointVal_axe4()
           
            node.axe4 = False
        
        if node.planPince_doigts:
            node.set_pose_goal_pince_doigts()
            
            node.planPince_doigts = False
        
        if node.planPince_main:
            node.set_pose_goal_pince_main()
            
            node.planPince_main = False

        node.send_to_arduino()
        time.sleep(0.7) #Pour ne pas encombrer le buffer de l'arduino, tester pour trouver la valeur la plus adaptée TODO
            
        adisplacement = node.displacement
        time.sleep(0.05)
        
    rospy.spin()