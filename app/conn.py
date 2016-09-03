#connect to database
import os, sqlite3
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
