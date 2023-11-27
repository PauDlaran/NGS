import cv2

def list_and_open_cameras():
    # Get the list of available cameras
    camera_indexes = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_indexes.append(i)
            cap.release()

    # Open the streams of each camera in different windows
    for index in camera_indexes:
        cap = cv2.VideoCapture(index)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow(f"Camera {index}", frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Call the function to list and open the cameras
list_and_open_cameras()
