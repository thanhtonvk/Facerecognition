import cv2
import os
from modules.FaceDetector import FaceDetector


class FaceDetection:
    def __init__(self):
        self.model = FaceDetector()

    def detect(self, image):
        faces, bboxes = self.model.detect(image)
        return {'faces': faces, 'boxes': bboxes}

    def save_face_from_video(self, id_sv, video):
        capture = cv2.VideoCapture(video)
        count = 0
        while (capture.isOpened()):
            ret, frame = capture.read()
            if ret == True:
                faces = self.detect(frame)['faces']
                for face in faces:
                    try:
                        os.mkdir(f"./faces/{id_sv}")
                        cv2.imwrite(f"./faces/{id_sv}/{count}.png", face)
                        print('create and save face')
                    except:
                        cv2.imwrite(f"./faces/{id_sv}/{count}.png", face)
                        print('save face')
                    count += 1
                if count > 1:
                    break
            else:
                break


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    face_detection = FaceDetection()
    image = cv2.imread('test/test2.jpg')
    result = face_detection.detect(image)
    plt.imshow(result['faces'][0])
    plt.show()
