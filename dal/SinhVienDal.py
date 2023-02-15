import sqlite3
from objects.SinhVien import SinhVien
from config import config
class SinhVienDal:
    def __init__(self):
        self.conn = sqlite3.connect(config.DATABASE)
    def insert(self,hoten):
        try:
            self.conn.execute("INSERT INTO SinhVien(hoten) values (?)",(hoten))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def update(self,sinhVien:SinhVien):            