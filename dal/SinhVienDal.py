import sqlite3
from objects.SinhVien import SinhVien
from config import config


class SinhVienDal:
    def __init__(self):
        pass
        

    def insert(self, hoten):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute(
                "INSERT INTO SinhVien(HoTen) values(?)", (hoten,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    def update(self, hoten, id):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute(
                "UPDATE SinhVien SET HoTen = ? where Id = ?", (hoten, id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return True

    def delete(self, id):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute("DELETE FROM SinhVien where Id = ?", (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return False

    def get(self):
        sinh_viens = []
        try:
            conn = sqlite3.connect(config.DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT * FROM SinhVien")
            rows = cur.fetchall()
            for row in rows:
                sv = SinhVien()
                sv.Id = row[0]
                sv.HoTen = row[1]
                sinh_viens.append(sv)
            conn.close()
            return sinh_viens
        except Exception as e:
            print('err ',e)
            return sinh_viens
