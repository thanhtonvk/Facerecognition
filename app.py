from flask import Flask, render_template, request,redirect
from werkzeug.utils  import secure_filename
from dal.DiemDanhDal import DiemDanhDal
from dal.SinhVienDal import SinhVienDal 
from modules.face_detection import FaceDetector
from modules.face_recognition import FaceRecognition
import os
from datetime import date
import cv2
app = Flask(__name__)

app.config['UPLOAD_VIDEO']   = './faces/'
diemDanhDal = DiemDanhDal()
sinhVienDal = SinhVienDal()
faceDetector = FaceDetector()
faceRecognition = FaceRecognition()

@app.route('/sinh-vien/them' , methods = ['GET','POST'])
def them_sv():
    if request.method == 'GET':
        return render_template('them_sinh_vien.html')
    if request.method == 'POST':
        ho_ten = request.form['ho_ten']
        sinhVienDal.insert(ho_ten)
        sinhVien = sinhVienDal.get()[-1]
        f = request.files['file']
        file_name = f.filename
        try:
            os.mkdir(app.config['UPLOAD_VIDEO']+"/videos/"+str(sinhVien.Id))
            save_path = os.path.join(app.config['UPLOAD_VIDEO']+"/videos/"+str(sinhVien.Id), file_name)
        except:
            print('err')
        f.save(save_path)
        faceDetector.save_face_from_video(sinhVien.Id,save_path)
        return redirect('/sinh-vien')
    return render_template('them_sinh_vien.html')
@app.route('/sinh-vien/xoa/<int:id>',methods=['GET'])
def xoa(id):
    sinhVienDal.delete(id)
    return redirect('/sinh-vien')    

@app.route('/sinh-vien', methods = ['GET'])
def danh_sach_sv():
    sinhViens = sinhVienDal.get()
    return render_template('danh_sach_sinh_vien.html',sinhViens = sinhViens)



@app.route('/',methods=['GET'])
def index():

    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    diemDanhs = diemDanhDal.get_by_date(current_date)
    return render_template('index.html',diemDanhs = diemDanhs)

@app.route('/diem-danh',methods=['GET','POST'])
def diem_danh():
    if request.method == 'GET':
        return render_template('diem_danh.html')
    if request.method == 'POST':
        f = request.files['file']
        file_name = f.filename
        save_path = os.path.join(app.config['UPLOAD_VIDEO']+"/images/", file_name)
        f.save(save_path)


        # load image
        frame = cv2.imread(save_path)
        predict = faceDetector.detect(frame)
        boxes = predict['boxes']
        faces = predict['faces']
        sinhViens = sinhVienDal.get()
        for idx, (x, y, w, h) in enumerate(boxes):
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face = faces[idx]
            sinh_vien = faceRecognition.search_face(face, sinhViens)
            if sinh_vien is not None:
                result = diemDanhDal.diem_danh(sinh_vien.Id)
                print('diem danh ',result)
        return redirect('/')
    return render_template('diem_danh.html')
if __name__ == '__main__':
    app.run(host='localhost', port=5000)


