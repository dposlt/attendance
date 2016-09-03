#add table into database

import sqlite3,os

class Conn:
    def __init__(self,dbname):
        self.dbname = dbname

    def tryConn(self):
        try:
            if os.path.exists(self.dbname):
                db = sqlite3.connect(self.dbname,check_same_thread=False)
                cursor = db.cursor()
                return (cursor,db)
            else:
                return False
        except IOError:
            return "Chyba souboru: ",sys.exc_info()[0]

class AddTable:
    zaznamy = Conn('dochazka.db')
    global conn,db
    (conn,db) = zaznamy.tryConn()

    def __init__(self, heslo):
	self.heslo = heslo

    def addTablePasswd(self):
	if conn:
		conn.execute("DROP TABLE IF EXISTS md5")
		conn.execute("CREATE table md5 (heslo)")
		db.commit()

    def addPasswdIntoTable(self):
    	if conn:
		import md5
		
		conn.execute("INSERT INTO md5 (heslo) VALUES (:heslo)", dict(heslo=md5.md5(self.heslo).hexdigest()))
		db.commit()

    def closeDb(self):
	if conn:
		conn.close()
		db.close()

add = AddTable('JelEn01+')
add.addTablePasswd()
add.addPasswdIntoTable()
add.closeDb()



