from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import cv2
import numpy as np


def build_model(path):
    return load_model(path)


def preprocess(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image,(128,128))
    image = preprocess_input(image)
    return image



class FaceRecognition:
    def __init__(self, path='./models/model.h5'):
        self.model = build_model(path)
    def compare(self,face_1, face_2):
        face_1 = preprocess(face_1)
        face_2 = preprocess(face_2)
        vector1 =  self.model.predict(np.expand_dims(face_1, 0),verbose = False)
        vector2 = self.model.predict(np.expand_dims(face_2, 0),verbose = False)
        return cosine_similarity(vector1, vector2)
    
