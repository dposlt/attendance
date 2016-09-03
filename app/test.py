import sqlite3

db = sqlite3.connect('dochazka.db')
cursor = db.cursor()
cursor.execute("select odchod from time where uzivatel=:user", dict(user='David Poslt'))
sloupec = len(cursor.fetchall())
row = cursor.fetchall()
print sloupec

for i in row:
    print i
cursor.close()
db.close()

