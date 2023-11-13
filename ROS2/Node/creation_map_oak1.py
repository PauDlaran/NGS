
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from gazebo_msgs.msg import ModelState
from cv_bridge import CvBridge
import cv2


class MyCameraNode(Node):

    def __init__(self):
        super().__init__('my_camera_node')

        # Souscrire au topic de l'image de la caméra
        self.camera_sub_ = self.create_subscription(
            Image, '/camera/image', self.camera_callback, 10)

        # Publier le topic de l'état du modèle
        self.model_state_pub_ = self.create_publisher(
            ModelState, '/gazebo/set_model_state', 10)

    def camera_callback(self, msg):
        # Convertir le message d'image en une image OpenCV
        bridge = CvBridge()
        try:
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except CvBridgeError as e:
            self.get_logger().error("CvBridge Error: %s" % e)
            return

        # Traiter l'image pour créer une carte 3D
        map_3d = self.process_image(cv_image)

        # Enregistrer la carte dans un fichier
        map_filename = "/path/to/map.pgm"
        cv2.imwrite(map_filename, map_3d)

        # Publier l'état du modèle à Gazebo
        model_state = ModelState()
        model_state.model_name = "my_robot"
        model_state.pose.position.x = 0.0
        model_state.pose.position.y = 0.0
        model_state.pose.position.z = 0.0
        model_state.pose.orientation.x = 0.0
        model_state.pose.orientation.y = 0.0
        model_state.pose.orientation.z = 0.0
        model_state.pose.orientation.w = 1.0
        model_state.reference_frame = "world"
        model_state.pose.position.z = 0.5  # Définir la hauteur du robot au-dessus du sol
        self.model_state_pub_.publish(model_state)

    def process_image(self, image):
        # TODO: Implémenter le traitement d'image pour créer une carte 3D
        map_3d = None
        return map_3d


def main(args=None):
    rclpy.init(args=args)
    node = MyCameraNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
