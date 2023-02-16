import cv2
import os

def get_model():
    faceCascade = cv2.CascadeClassifier('./models/face_detection.xml')
    return faceCascade


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def crop_face(image, faces):
    images = []
    for (x, y, w, h) in faces:
        x_min = x
        y_min = y
        x_max = x+w
        y_max = y+h
        images.append(image[y_min:y_max, x_min:x_max])
    return images


class FaceDetector:
    def __init__(self):
        self.model = get_model()

    def detect(self, image):
        gray_image = preprocess(image)
        faces = self.model.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(15, 15),
            flags=cv2.CASCADE_SCALE_IMAGE)
        return {'faces': crop_face(image, faces), 'boxes': faces}
    
    def save_face_from_video(self, id_sv, video):
        capture = cv2.VideoCapture(video)
        count = 0
        while(capture.isOpened()):
            # Capture frame-by-frame
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
                if count > 4:
                    break
           # Break the loop
            else:
                break


if __name__ == '__main__':
    face_detector = FaceDetector()
    image = cv2.imread('./test/test.jpg')
    print(face_detector.detect(image))
