# -*- coding: utf-8 -*-

''' prichod a odchodu
    datum: 22.7.2014
    verze: 1.0.
'''


class Dochazka:
    import conn
    pripojDb = conn.Conn('dochazka.db')
    (conn,db) = pripojDb.tryConn()
        
    
    def prichod(self,user,prichod,stav):
        self.user = user
        self.prichod = prichod
        self.stav = stav
        
        
        overOdchod = Dochazka().overOdchod(self.user)
                
        self.conn.execute("INSERT INTO time (uzivatel,prichod) VALUES ('{0}','{1}')".format(self.user, self.prichod))
        
        self.conn.execute("INSERT INTO stav (uzivatel,cas,stav) VALUES ('{0}','{1}','{2}')".format(self.user,self.prichod,self.stav))

        self.db.commit()


    def overOdchod(self,user):
        self.user = user
        
        self.conn.execute("SELECT id FROM time WHERE id=(SELECT MAX(id) FROM time where uzivatel='{user}')".format(user=self.user))
        maxID = self.conn.fetchone()
    
        if maxID:
            maxID = int(maxID[0])
            self.conn.execute("SELECT odchod FROM time WHERE id='{id}'".format(id=maxID))
            odchod = self.conn.fetchone()
            
            if odchod[0] is None:
                self.conn.execute("UPDATE time SET odchod='{odchod}' WHERE id = '{id}'".format(odchod='Chyba odchodu',id=maxID))
                self.db.commit()
        else:
            return False

    def odchody(self,user, odchod,stav):
        self.user = user
        self.odchod = odchod
        self.stav = stav
        
        self.conn.execute("SELECT id FROM time WHERE id=(SELECT MAX(id) FROM time where uzivatel='{user}')".format(user=self.user))
        maxID = self.conn.fetchone()[0]
        if maxID:
            self.conn.execute("UPDATE time SET odchod='{odchod}' WHERE id = '{id}'".format(odchod=self.odchod,id=maxID))
            self.conn.execute("INSERT INTO stav (uzivatel,cas,stav) VALUES ('{0}','{1}','{2}')".format(self.user,self.odchod,self.stav))
            self.db.commit()
            
