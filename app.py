import os
from datetime import date

from flask import Flask, render_template, request, redirect


from dal.NguoiDungDal import NguoiDungDal
from modules.face_detection import FaceDetection
from modules.face_recognition import FaceRecognition

app = Flask(__name__)

app.config['UPLOAD_VIDEO'] = './faces/'
NguoiDungDal = NguoiDungDal()
faceDetector = FaceDetection()
faceRecognition = FaceRecognition()


@app.route('/nguoi-dung/them', methods=['GET', 'POST'])
def them_sv():
    if request.method == 'GET':
        return render_template('them_nguoi_dung.html')
    if request.method == 'POST':
        ho_ten = request.form['ho_ten']
        NguoiDungDal.insert(ho_ten)
        NguoiDung = NguoiDungDal.get()[-1]
        f = request.files['file']
        file_name = f.filename
        try:
            os.mkdir(app.config['UPLOAD_VIDEO'] + "/videos/" + str(NguoiDung.Id))
            save_path = os.path.join(app.config['UPLOAD_VIDEO'] + "/videos/" + str(NguoiDung.Id), file_name)
        except:

            print('err')
        f.save(save_path)
        faceDetector.save_face_from_video(NguoiDung.Id, save_path)
        return redirect('/')
    return render_template('them_nguoi_dung.html')


@app.route('/nguoi-dung/xoa/<int:id>', methods=['GET'])
def xoa(id):
    NguoiDungDal.delete(id)
    return redirect('/nguoi-dung')


@app.route('/', methods=['GET'])
def danh_sach_sv():
    NguoiDungs = NguoiDungDal.get()
    return render_template('danh_sach_nguoi_dung.html', NguoiDungs=NguoiDungs)



if __name__ == '__main__':
    app.run(host='localhost', port=5000)
