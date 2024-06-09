# import các thư viện
import cv2
import os
from modules.FaceDetector import FaceDetector


class FaceDetection:
    def __init__(self):
        # tải mô hình phát hiện khuôn mặt
        self.model = FaceDetector()

# phát hiện khuôn mặt, câu lệnh này trả về khuôn mặt và các box chứa khuôn mặt
    def detect(self, image):
        faces, bboxes = self.model.detect(image)
        return {'faces': faces, 'boxes': bboxes}
# lưu các khuôn mặt vào trong thư mục
    def save_face_from_video(self, id_sv, video):
        # đọc video 
        capture = cv2.VideoCapture(video)
        count = 0
        # đọc từng ảnh trong video
        while (capture.isOpened()):
            ret, frame = capture.read()
            if ret == True:
                # phát hiện khuôn mặt trong video
                faces = self.detect(frame)['faces']
                for face in faces:
                    # lưu các khuôn mặt vào trong thư mục faces
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
