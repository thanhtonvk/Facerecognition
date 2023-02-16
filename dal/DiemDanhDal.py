import sqlite3
from objects.DiemDanh import DiemDanh
from config import config
from datetime import date


def kiem_tra_diem_danh(id_sv, diem_danhs):
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    for diem_danh in diem_danhs:
        if id_sv == diem_danh.IdSinhVien and diem_danh.NgayDiemDanh == current_date:
            return False
    return True


class DiemDanhDal:
    def __init__(self):
        pass

    def get_by_date(self, ngay_diem_danh):
        query = "select DiemDanh.Id,HoTen,NgayDiemDanh,IdSinhVien from DiemDanh,SinhVien where SinhVien.Id = DiemDanh.IdSinhVien and DiemDanh.NgayDiemDanh = ?"
        diem_danhs = []
        try:
            conn = sqlite3.connect(config.DATABASE)
            cur = conn.cursor()
            cur.execute(query, (ngay_diem_danh,))
            rows = cur.fetchall()
            for row in rows:
                diem_danh = DiemDanh()
                diem_danh.Id = row[0]
                diem_danh.TenSV = row[1]
                diem_danh.NgayDiemDanh = row[2]
                diem_danh.IdSinhVien = row[3]
                diem_danhs.append(diem_danh)
            conn.close()
            return diem_danhs
        except Exception as e:
            print(e)
            return diem_danhs

    def get_all(self):
        query = "select DiemDanh.Id,HoTen,NgayDiemDanh,IdSinhVien from DiemDanh,SinhVien where SinhVien.Id = DiemDanh.IdSinhVien"
        diem_danhs = []
        try:
            conn = sqlite3.connect(config.DATABASE)
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                diem_danh = DiemDanh()
                diem_danh.Id = row[0]
                diem_danh.TenSV = row[1]
                diem_danh.NgayDiemDanh = row[2]
                diem_danh.IdSinhVien = row[3]
                diem_danhs.append(diem_danh)
            conn.close()
            return diem_danhs
        except Exception as e:
            print(e)
            return diem_danhs

    def diem_danh(self, id_sv):
        query = "insert into DiemDanh(IdSinhVien,NgayDiemDanh) values(?,?)"
        if kiem_tra_diem_danh(id_sv):
            try:
                conn = sqlite3.connect(config.DATABASE)
                today = date.today()
                current_date = today.strftime("%d/%m/%Y")
                conn.execute(query, (id_sv, current_date,))
                conn.commit()
                conn.close()
                return True
            except Exception as e:
                print(e)
                return False
        return False
