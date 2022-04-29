import pandas as pd
import requests
import lxml
import csv
import sqlite3
import hashlib


r = requests.get('http://irsc.ut.ac.ir/index.php?page=1&lang=fa')
df = pd.read_html(r.text)[9]
df.to_csv('irsc.csv', index=False)


file = open('irsc.csv')
csvreader = csv.reader(file)
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
file.close()


conn = sqlite3.connect('irsc.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS irsc')
cur.execute("""CREATE TABLE IF NOT EXISTS irsc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area Text ,
    length Text ,
    width Text ,
    depth Text ,
    amplitude Text ,
    time Text ,
    flag Text ,
    hash Text );""")
conn.commit()


def Insert_Data ():

    for i in range(1, len(rows)):

        time = str(rows[i][0])
        depth = str(rows[i][1])
        width = str(rows[i][2])
        length = str(rows[i][3])
        amplitude = str(rows[i][4])
        area = str(rows[i][5])
        flag = 'False'


        twt = (" زلزله ای به بزرگی "+ depth +" به وقت محلی "+ time +" در عرض جغرافیایی "+ width +" و طول جغرافیایی "+ length +" در عمق "+ amplitude +" کیلومتری منطقه "+ area +" را لرزاند ")
        this_hash_obj = hashlib.sha256(twt.encode())
        twt_hash = this_hash_obj.hexdigest()
        number = i

        query = f'INSERT INTO irsc VALUES ("{number}", "{area}", "{length}", "{width}", "{depth}", "{amplitude}", "{time}","{flag}", "{twt_hash}")'
        print(query)
        cur.execute(query)
        conn.commit()

    conn.close()


Insert_Data()


