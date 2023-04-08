import sqlite3
import os.path

This_folder = os.path.dirname(os.path.abspath(__file__))
DB_file = os.path.join(This_folder, "webScrape.sqlite")
conn = sqlite3.connect(DB_file)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = on")


def createTable():
    c.execute(
        """CREATE TABLE IF NOT EXISTS laptop(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        isim        TEXT,
        marka       TEXT,
        model_no    TEXT,
        OS          TEXT DEFAULT FreeDOS,
        ram         INTEGER,
        disk_tur    TEXT,
        disk_cap    INTEGER,
        ekran       REAL,
        islemci     TEXT,
        ekran_karti TEXT,
        site        TEXT REFERENCES siteler (siteisim),
        link        TEXT,
        fiyat       REAL,
        puan        REAL)""")
    c.execute(
        """CREATE TABLE IF NOT EXISTS siteler (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    siteisim TEXT    UNIQUE NOT NULL)"""
    )
    conn.commit()


def addlaptop(productname, productbrand, productmodel, productos, productram, productdisk, productspace, productscreen,
              productcpu, productgpu, productpage, productlink, productprice, productrating):
    print("addlaptop")
    c.execute("INSERT INTO laptop "
              "(isim, marka, model_no, OS, ram, disk_tur, disk_cap, ekran, islemci, ekran_karti, site, link, fiyat, puan) "
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (productname, productbrand, productmodel, productos, productram, productdisk, productspace,
               productscreen, productcpu, productgpu, productpage, productlink, productprice, productrating))
    conn.commit()


def checkduplicate(site, pageurl):
    c.execute("""SELECT link
              FROM laptop
              WHERE site = ?
              AND link = ?""", (site, pageurl,))
    data = c.fetchall()
    if data:
        return True
    else:
        return False

def checkmodel(site, productmodel):
    c.execute("""SELECT model_no
              FROM laptop
              WHERE site = ?
              AND model_no = ?""", (site, productmodel,))
    data = c.fetchall()
    if data:
        return True
    else:
        return False
def addModelFromExistingModel(productname):
    c.execute("""SELECT DISTINCT model_no
              FROM laptop
              where model_no != ''""")
    allmodels = c.fetchall()
    for model in allmodels:
        if model[0] in productname:
            return model[0]

def DBmain():
    createTable()
    # conn, c = connect()
    # c.execute("CREATE TABLE IF NOT EXISTS amazon (id INTEGER PRIMARY KEY, marka TEXT, model TEXT, ram TEXT, hdd TEXT, ekran TEXT)")
    # conn.commit()
    # conn.close()

DBmain()