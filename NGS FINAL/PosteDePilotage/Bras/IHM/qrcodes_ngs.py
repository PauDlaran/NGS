import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from pyzbar.pyzbar import decode

class VideoSubscriber:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_received = False
        self.image = None

        # rospy.init_node('video_subscriber', anonymous=True)
        rospy.Subscriber("/Cam1", Image, self.image_callback)

    def image_callback(self, msg):
        # Convertir l'image ROS en image OpenCV
        self.image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        self.image_received = True

    def get_video_frame(self):
        # Attendre jusqu'à ce que l'image soit reçue
        while not self.image_received:
            rospy.sleep(0.1)
        # Récupérer l'image reçue
        return self.image
    

    def readQrCode(self, frame):
        print("on est de lautre cote")
        
        # while True:
        # Decode QR codes from the frame
        print("Dans le whiel")
        self.qr_codes = decode(frame)
        # print("frame : ")
        # print(frame)
        # print("decode : ")
        # print(self.qr_codes)
        
        if self.qr_codes:
            print("on a un truc")
            # Si un code QR est trouvé, renvoyer les données du premier code QR trouvé
            return self.qr_codes[0].data.decode("utf-8")

        else:
            # Si aucun code QR n'est trouvé, renvoyer None
            print("ya r")
            return None
                    

# if __name__ == '__main__':
#     try:
#         print("a")
#         video_subscriber = VideoSubscriber()

#         while not rospy.is_shutdown():
#             # Récupérer le frame vidéo
#             print("aa")
#             frame = video_subscriber.get_video_frame()
#             print("aaa")
#             # Lire le code QR
#             qr_data = video_subscriber.readQrCode(frame)
#             print("a")
#             if qr_data:
#                 print("QR Code Data:", qr_data)
#                 break

#             # Attendre jusqu'à ce que 'q' soit pressé pour quitter la boucle
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # Fermer toutes les fenêtres OpenCV
#         cv2.destroyAllWindows()

#     except rospy.ROSInterruptException:
#         pass
