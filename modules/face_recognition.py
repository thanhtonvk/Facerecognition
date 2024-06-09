import os

import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from utils import onnx_model_inference

tiền xử lý dữ liệu, thay đổi kícch thước ảnh về 112*112
# chuẩn hóa dữ liệu về (0,1) ban đầu hình ảnh sẽ là (0-255)
def preprocess(image):
    image = cv2.resize(image,(112,112))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image = image / 255.0
    image = image.transpose(2, 0, 1)
    image = np.expand_dims(image, 0)
    return image


class FaceRecognition:
    # tải mô hình nhận diện khuôn mặt
    def __init__(self, path='models/w600k_mbf.onnx'):
        self.model = onnx_model_inference(path)

# lây ra đặc trưng khuôn mặt
    def get_embed(self, face):
        output = self.model.run(None, {self.model.get_inputs()[0].name: face})[0]
        return output
# so sánh đặc trưng khuôn mặt, dùng công thức tính cosine_similarity
# dữ liệu so sánh trả về 0-1 tương đương 0%-100%
    def compare(self, face_1, face_2):
        face_1 = preprocess(face_1)
        face_2 = preprocess(face_2)

        vector1 = self.get_embed(face_1)
        vector2 = self.get_embed(face_2)
        return cosine_similarity(vector1, vector2)
# tìm kiếm khuôn mặc tương ứng bằng cách so sánh mặt được quét với mặt ở trong cơ sở dữ liệu, nếu độ giống nhau 0.5 trở lên thì sẽ là trùng
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
