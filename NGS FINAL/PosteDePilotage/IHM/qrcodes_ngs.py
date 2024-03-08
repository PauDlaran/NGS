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
        
        # Decode QR codes from the frame
        self.qr_codes = decode(frame)
        
        if self.qr_codes:
            # Si un code QR est trouvé, renvoyer les données du premier code QR trouvé
            return self.qr_codes[0].data.decode("utf-8")

        else:
            # Si aucun code QR n'est trouvé, renvoyer None
            return None
                    