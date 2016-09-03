#overeni hesla

import sqlite3,os,md5

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

class OverHeslo:
    zaznamy = Conn('dochazka.db')
    global conn,db
    (conn,db) = zaznamy.tryConn()

    def __init__(self, heslo):
        self.heslo = heslo

    def over(self):
        conn.execute('SELECT * FROM md5')
        password = conn.fetchone()
        heslo = md5.md5(self.heslo).hexdigest()
        
        if heslo == password[0]:
            return True
        else:
            return False

    def closedb(self):
        conn.close()
        db.close()


