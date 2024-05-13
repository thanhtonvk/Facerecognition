import os

import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from utils import onnx_model_inference


def preprocess(image):
    image = cv2.resize(image,(112,112))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image = image / 255.0
    image = image.transpose(2, 0, 1)
    image = np.expand_dims(image, 0)
    return image


class FaceRecognition:
    def __init__(self, path='models/w600k_mbf.onnx'):
        self.model = onnx_model_inference(path)

    def get_embed(self, face):
        output = self.model.run(None, {self.model.get_inputs()[0].name: face})[0]
        return output

    def compare(self, face_1, face_2):
        face_1 = preprocess(face_1)
        face_2 = preprocess(face_2)

        vector1 = self.get_embed(face_1)
        vector2 = self.get_embed(face_2)
        return cosine_similarity(vector1, vector2)

    def search_face(self, current_face, nguoi_dungs):
        for nguoi_dung in nguoi_dungs:
            path = f"./faces/{nguoi_dung.Id}"
            if os.path.exists(path):
                file_names = os.listdir(path)
                for file in file_names:
                    face = cv2.imread(f"{path}/{file}")
                    cos_sim = self.compare(current_face, face)
                    if cos_sim > 0.5:
                        return nguoi_dung
        return None


if __name__ == '__main__':
    image = cv2.imread('faces/3/4.png')
    image = cv2.resize(image, (112, 112))
    image1 = cv2.imread('faces/3/0.png')
    image1 = cv2.resize(image1, (112, 112))
    face_search = FaceRecognition()
    print(face_search.compare(image, image1))
