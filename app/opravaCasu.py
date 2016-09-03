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

class OpravaDochazky:
    zaznamy = Conn('dochazka.db')
    global conn,db
    (conn,db) = zaznamy.tryConn()

    def __init__(self,prichod,odchod,idPozadavku):
        self.prichod = prichod
        self.odchod = odchod
        self.idPozadavku = idPozadavku

    def doRepair(self):
        conn.execute('UPDATE time SET prichod=:prichod, odchod=:odchod WHERE ID = :idPozadavku',
                     dict(prichod = self.prichod, odchod = self.odchod, idPozadavku = self.idPozadavku))
        db.commit()
    
    def doRepairCas(self):
	#zjistime cas prichodu a odchodu
	import datetime
	conn.execute("select prichod, odchod from time where id=:id",dict(id=self.idPozadavku))
        row = conn.fetchone()
        prichod = row[0]
        odchod = row[1]
        
        start = prichod[11:19]
        end = odchod[11:19]
        start_dt = datetime.datetime.strptime(start, '%H:%M:%S')
        end_dt = datetime.datetime.strptime(end, '%H:%M:%S')
        diff = (end_dt - start_dt)
        result = str(datetime.timedelta(seconds=diff.seconds/60))
	
	#upravime cas
	conn.execute("UPDATE time set odpracovano=:hodiny WHERE ID=:idPozadavku", dict(hodiny = result[2:], idPozadavku=self.idPozadavku))
	db.commit() 

    def showData(self):
        conn.execute('SELECT id,prichod,odchod FROM time WHERE ID = :idPozadavku', dict(idPozadavku = self.idPozadavku))
        row = conn.fetchone()
        return row

