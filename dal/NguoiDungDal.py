import sqlite3
from objects.NguoiDung import NguoiDung
from config import config


class NguoiDungDal:
    def __init__(self):
        pass
        

    def insert(self, hoten):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute(
                "INSERT INTO NguoiDung(HoTen) values(?)", (hoten,))
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
                "UPDATE NguoiDung SET HoTen = ? where Id = ?", (hoten, id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print('err ', e)
            return True

    def delete(self, id):
        try:
            conn = sqlite3.connect(config.DATABASE)
            conn.execute("DELETE FROM NguoiDung where Id = ?", (id,))
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
            cur.execute("SELECT * FROM NguoiDung")
            rows = cur.fetchall()
            for row in rows:
                sv = NguoiDung()
                sv.Id = row[0]
                sv.HoTen = row[1]
                sinh_viens.append(sv)
            conn.close()
            return sinh_viens
        except Exception as e:
            print('err ',e)
            return sinh_viens
