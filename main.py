from modules.face_detection import FaceDetector
from modules.face_recognition import FaceRecognition
from dal.SinhVienDal import SinhVienDal
from dal.DiemDanhDal import DiemDanhDal
import cv2
if __name__ == '__main__':
    face_detector = FaceDetector()
    face_recognition = FaceRecognition()

    diem_danh_dal = DiemDanhDal()

    # lấy về danh sách sinh viên
    sinh_vien_dal = SinhVienDal()
    sinh_viens = sinh_vien_dal.get()

    # define a video capture object
    vid = cv2.VideoCapture(0)

    count = 0
    while(True):
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        predict = face_detector.detect(frame)
        boxes = predict['boxes']
        faces = predict['faces']
        for idx, (x, y, w, h) in enumerate(boxes):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face = faces[idx]
            sinh_vien = face_recognition.search_face(face, sinh_viens)
            if sinh_vien is not None:
                if diem_danh_dal.diem_danh(sinh_vien.Id):
                    cv2.putText(frame, f"{sinh_vien.HoTen}-{sinh_vien.Id} : Thanh cong",
                                (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
                else:
                    cv2.putText(frame, f"{sinh_vien.HoTen}-{sinh_vien.Id} : Da diem danh",
                                (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.imshow('Điểm danh bằng khuôn mặt', frame)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
