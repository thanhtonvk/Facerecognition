import cv2
import unidecode
from dal.NguoiDungDal import NguoiDungDal
from modules.face_detection import FaceDetection
from modules.face_recognition import FaceRecognition
from modules.qr_detection import QRDetection

import threading


SEND_DATA = False


if SEND_DATA:
    import serial
    import time
    NAME_COM = 'COM4'
    PORT = 280301
    dataSerial = serial.Serial(NAME_COM, PORT, timeout=.1)
    def send_data(id):
        time.sleep(3)
        dataSerial.write(str(id).encode())
        print('mo khoa ',id)
        time.sleep(3)

id = -1

if __name__ == '__main__':
    face_detector = FaceDetection()
    face_recognition = FaceRecognition()
    qr_detection = QRDetection()

    nguoi_dung_dal = NguoiDungDal()
    nguoi_dungs = nguoi_dung_dal.get()

    vid = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    count = 0
    while (True):
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        qr_result = qr_detection.detect(frame)
        if qr_result is not None:
            content = qr_result.get('value').strip()
            x_min, y_min, x_max, y_max = qr_result.get('bbox')
            if len(content) == 0:
                cv2.putText(frame, f"QR bi mo, khong the doc",
                            (x_min, y_min), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                nguoi_dung = qr_detection.search_qr(frame, nguoi_dungs)
                if nguoi_dung is not None:
                    cv2.rectangle(frame, (x_min, y_min),
                                  (x_max, y_max), (0, 0, 255), 2)
                    cv2.putText(frame, f"ID:{nguoi_dung.Id} {unidecode.unidecode(nguoi_dung.HoTen)}",
                                (x_min, y_min), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    if SEND_DATA:
                        thread = threading.Thread(
                            target=send_data, args=(nguoi_dung.Id,))
                        thread.start()
                else:
                    cv2.rectangle(frame, (x_min, y_min),
                                  (x_max, y_max), (0, 0, 255), 2)

        predict = face_detector.detect(frame)
        boxes = predict['boxes']
        faces = predict['faces']
        for idx, (x, y, w, h) in enumerate(boxes):
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
            face = faces[idx]
            nguoi_dung = face_recognition.search_face(face, nguoi_dungs)
            if nguoi_dung is not None:
                cv2.putText(frame, f"ID:{nguoi_dung.Id} {unidecode.unidecode(nguoi_dung.HoTen)}",
                            (x, y), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
                if SEND_DATA:
                    thread = threading.Thread(
                        target=send_data, args=(nguoi_dung.Id,))
                    thread.start()
        cv2.imshow('Nhan dien khuon mat', frame)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
