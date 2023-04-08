import sqlite3
import os.path
import random

This_folder = os.path.dirname(os.path.abspath(__file__))
DB_file = os.path.join(This_folder, "webScrape.sqlite")
conn = sqlite3.connect(DB_file)
c1 = conn.cursor()
laptopcumpath = os.path.dirname((os.path.abspath(__file__))) + os.sep + 'laptopcum'
cimripath = os.path.dirname((os.path.abspath(__file__))) + os.sep + 'cimri-clone'

choose = int(input('1 for laptopcum, 2 for cimri: '))
if choose == 1:
    # e-ticaret clone
    c1.execute(
        'SELECT id, isim, marka, model_no, OS, islemci, ekran_karti, disk_tur, '
        'ram, disk_cap, ekran, fiyat, puan from laptop')
    DB2_file = os.path.join(laptopcumpath, "db.sqlite3")
    conn2 = sqlite3.connect(DB2_file)
    c2 = conn2.cursor()
    c2.execute('DELETE FROM laptop_laptop;', )
    for i in c1.fetchmany(200):
        data_tuple = i
        data_list = list(data_tuple)
        data_list[11] = ((float(data_list[11])) - (random.randint(-500, +500)))
        sqlite_insert_with_param = '''INSERT INTO laptop_laptop(id, name, brand, model ,operating_system, cpu, gpu, disc_type, ram, disc, screen_size, price, rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,?);'''
        c2.execute(sqlite_insert_with_param, data_list)
        conn2.commit()
elif choose == 2:
    # cimri clone
    c1.execute(
        'SELECT id, isim, marka, model_no, OS, islemci, ekran_karti, disk_tur, ram, '
        'disk_cap, ekran, fiyat, puan, site, link from laptop')
    DB2_file = os.path.join(cimripath, "db.sqlite3")
    conn2 = sqlite3.connect(DB2_file)
    c2 = conn2.cursor()
    c2.execute('DELETE FROM laptop_laptop;', )
    for i in c1.fetchall():
        sqlite_insert_with_param = '''INSERT INTO laptop_laptop(id, name, brand, model ,operating_system, cpu, gpu, disc_type, ram, disc, screen_size, price, rating, site, site_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,?, ?, ?);'''
        c2.execute(sqlite_insert_with_param, i)
        conn2.commit()
print('done')
