import cv2


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


if __name__ == '__main__':
    face_detector = FaceDetector()
    image = cv2.imread('./test/test.jpg')
    print(face_detector.detect(image))
