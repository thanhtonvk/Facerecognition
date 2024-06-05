import os
from flask import Flask, render_template, request, redirect
import cv2

from dal.NguoiDungDal import NguoiDungDal
from modules.face_detection import FaceDetection
from modules.face_recognition import FaceRecognition
import pathlib
app = Flask(__name__)

app.config['UPLOAD_VIDEO'] = './faces/'
NguoiDungDal = NguoiDungDal()
faceDetector = FaceDetection()
faceRecognition = FaceRecognition()


@app.route('/nguoi-dung/them', methods=['GET', 'POST'])
def them_sv():
    if request.method == 'GET':
        return render_template('them_nguoi_dung.html')
    ho_ten = request.form['ho_ten']
    id = request.form['id']
    NguoiDungDal.insert(ho_ten, id)

    f = request.files['file']
    file_name = f.filename
    pathlib.Path(app.config['UPLOAD_VIDEO'] + "/videos/" +
                 str(id)).mkdir(exist_ok=True)
    save_path = os.path.join(
        app.config['UPLOAD_VIDEO'] + "/videos/" + str(id), file_name)
    f.save(save_path)
    faceDetector.save_face_from_video(id, save_path)
    return redirect('/')


@app.route('/nguoi-dung/them-qr', methods=['GET', 'POST'])
def them_qr():
    if request.method == 'GET':
        return render_template('them_nguoi_dung_qr.html',name="")
    ho_ten = request.form['ho_ten']
    id = request.form['id']
    f = request.files['file']
    pathlib.Path("./qrs/" + str(id)).mkdir(exist_ok=True)
    save_path = os.path.join("./qrs/" + str(id), 'qr.png')
    f.save(save_path)
    qrCodeDetector = cv2.QRCodeDetector()
    image = cv2.imread(save_path)
    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
    if points is None:
        return render_template('them_nguoi_dung_qr.html',name="Không đọc được QR")
    NguoiDungDal.insert(ho_ten, id)
    return redirect('/')


@app.route('/nguoi-dung/xoa/<int:id>', methods=['GET'])
def xoa(id):
    NguoiDungDal.delete(id)
    return redirect('/')


@app.route('/', methods=['GET'])
def danh_sach_sv():
    NguoiDungs = NguoiDungDal.get()
    return render_template('danh_sach_nguoi_dung.html', NguoiDungs=NguoiDungs)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
