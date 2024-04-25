import sqlite3
conn = sqlite3.connect('./database/database.sqlite')

conn.execute("""CREATE TABLE IF NOT EXISTS NguoiDung(
    Id integer primary key AUTOINCREMENT,
    HoTen text not null
);""")
conn.commit()
conn.close()


from dal.NguoiDungDal import NguoiDungDal
dal = NguoiDungDal()

print(dal.get())