import sqlite3
conn = sqlite3.connect('./database/database.sqlite')

conn.execute("""CREATE TABLE IF NOT EXISTS SinhVien(
    Id integer primary key AUTOINCREMENT,
    HoTen text not null
);""")
conn.execute("""CREATE TABLE IF NOT EXISTS DiemDanh(
    Id integer primary key AUTOINCREMENT,
    IdSinhVien integer NOT NULL,
    NgayDiemDanh text NOT NULL
);""")
conn.commit()
conn.close()


from dal.SinhVienDal import SinhVienDal
dal = SinhVienDal()


print(dal.get())