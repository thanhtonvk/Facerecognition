import cv2
import os


class QRDetection:
    # tải mô hình phát hiện QR và đọc QR
    qrCodeDetector = cv2.QRCodeDetector()
    # phát hiện và đọc nội dung từ mã QR

    def detect(self, image):
        decodedText, points, _ = self.qrCodeDetector.detectAndDecode(image)
        if points is None:
            return None
        x1, y1 = tuple(points[0][0].astype('int'))
        x2, y2 = tuple(points[0][1].astype('int'))
        x3, y3 = tuple(points[0][2].astype('int'))
        x4, y4 = tuple(points[0][3].astype('int'))

        x_min = min(x1, x2, x3, x4)
        y_min = min(y1, y2, y3, y4)
        x_max = max(x1, x2, x3, x4)
        y_max = max(y1, y2, y3, y4)
        return {'value': str(decodedText), 'bbox': (x_min, y_min, x_max, y_max)}

# so khớp mã QR quét với các mã QR đã có trong CSDL, nếu trùng thì sẽ trả về ổ khóa tương ứng
    def search_qr(self, current_qr, nguoi_dungs):
        # đọc nội dung từ QR
        current_result = self.detect(current_qr)

        if current_result is not None:
            current_value = current_result.get('value')
            # tìm kiếm và so khớp các mã QR khác trong CSDL 
            for nguoi_dung in nguoi_dungs:
                path = f"qrs/{nguoi_dung.Id}"
                if os.path.exists(path):
                    file_names = os.listdir(path)
                    for file in file_names:
                        image = cv2.imread(f"{path}/{file}")
                        result_detect = self.detect(image)
                        print(result_detect)
                        if result_detect is not None:
                            value = result_detect['value']
                            if value == current_value:
                                return nguoi_dung
        return None
