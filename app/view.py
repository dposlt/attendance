#-*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, Response
import database, time, pdf, overeniHesla, validace
from datetime import datetime

import sys
from orca.braille import refresh

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


@app.route('/')
def uzivatele():
    db = database.openDatabase().conn()
    if db == False:
        return render_template('uzivatele.html', db=False)
    row = database.openDatabase().selectUser()
    if row:
        return render_template('uzivatele.html', db=True, row=row)
    else:
        return render_template('uzivatele.html', db=True, row=False)

	 
@app.route('/database')
def createdb():
	 return render_template('database.html', root=True)


@app.route('/database', methods=['GET', 'POST'])
def createdb_post():
    passwd = request.form['pass']
    secretepass = 'JelEn01+'
    if request.method == 'POST':
        if len(passwd) == 0:
            return render_template('database.html', root=True, create=u'Zadejte platné heslo')
        if passwd != secretepass:
            return render_template('database.html', root=True, create=u'Zadané heslo je neplatné')

        create = database.openDatabase().createDb('dochazka.db')
        if create:
            return render_template('database.html', root=True, create=u'Databáze obnovena')


@app.route('/admin')
def admin():
    return render_template('admin.html', root=True)


@app.route('/newuser')
def newuser():
    return render_template('newuser.html', root=True)


@app.route('/newuser', methods=['GET', 'POST'])
def newuser_post():
    name = request.form['name']
    if request.method == 'POST':
        if len(name) == 0:
            return render_template('newuser.html', root=True, create=u'Pole musíte vyplnit')
        user = database.openDatabase().createUser(name)
        if user == False:
            return render_template('newuser.html', root=True, create=u'Uživatel již existuje')
        else:
            return render_template('newuser.html', root=True, create=u'Uloženo')


@app.route('/deluser')
def deluser():
    row = database.openDatabase().selectUser()
    if row == False:
        return render_template('deluser.html', root=True, row=False)
    return render_template('deluser.html', root=True, row=row)


@app.route('/deluser', methods=['GET', 'POST'])
def deluser_post():
    name = request.form['jmeno']
    if request.method == 'POST':
        user = database.openDatabase().delUser(name)
        if user:
            return render_template('deluser.html', root=True, create=u'uživatel odstraněn')


def diakritika(vstup):
        #odstraneni diakritiky
    import unicodedata
    vstup = unicode(vstup)
    vstup = unicodedata.normalize('NFKD', vstup)

    output = ''
    for c in vstup:
        if not unicodedata.combining(c):
            output += c
    return output

@app.route('/named')
def named():
    global name
    name = request.args.get('name')   
    if len(name) > 0:
        return render_template('named.html', root=False, jmeno=name)


@app.route('/named', methods=['GET', 'POST'])
def named_post():
    currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    currentDate = datetime.now().strftime('%Y-%m-%d')
    import prichody
    names = diakritika(name)
    if request.method == 'POST':
        if request.form.get('submit') == u'příchod':
            stav = 'příchod'
            prichod = prichody.Dochazka()
            prichod.prichod(names,currentTime, stav)
            # database.openDatabase().insertArrive(name,currentTime,stav)
            return render_template('named.html', root=False, jmeno=name, css_time="time",
                                   time=u"Příchod: " + currentTime, wait="countdown", odpocet=True)


        elif request.form.get('submit') == 'odchod':
            stav = 'odchod'
            # musíme zjistit zdali uživatel vůbec přišel jinak asi moc odejít nemůže
            row = database.openDatabase().insertLeave(names, currentTime, currentDate + '%')
            if row:
                odchod = prichody.Dochazka()
                odchod.odchody(names,currentTime,stav)
                return render_template('named.html', root=False, jmeno=name, css_time="time",
                                       time="Odchod: " + currentTime, wait="countdown", odpocet=True)
            else:
                return render_template('named.html', root=False, jmeno=name, css_time="time",
                                       time=u"Není možno odejít před příchodem", wait="countdown", odpocet=False)


@app.route('/prehled')
def prehled():
    row = database.openDatabase().selectPristupy()
    if row:
        return render_template('pristup.html', root=True, row=row)
    else:
        return render_template('pristup.html', root=True, row=False)


@app.route('/filter')
def filter():
    global row
    row = database.openDatabase().selectUser()
    if row:
        return render_template('filter.html', root=True, row=row, filter=True)
    else:
        return render_template('filter.html', root=True, row=False)
    

@app.route('/filter', methods=['GET', 'POST'])
def filter_post():
    user = request.form['jmeno']
    user = diakritika(user)
    od = request.form['from']
    do = request.form['to']
    if request.method == 'POST':
        if request.form.get('submit') == u'Filtrovat':
            try:
                if len(od) != 0 and len(do) != 0:
                    dotaz = database.openDatabase().selectFilter(
                        'SELECT uzivatel,prichod,odchod,odpracovano FROM time WHERE prichod BETWEEN :prichod AND :odchod AND uzivatel=:user',
                        dict(prichod=od, odchod=do, user=user))
                    return render_template('filter.html', root=True, row=row, filter=True, more=dotaz,
                                           celkem=database.openDatabase().celkem(dotaz), od=od, do=do, selected=user)

                elif len(od) != 0:
                    dotaz = database.openDatabase().selectFilter(
                        'SELECT uzivatel,prichod,odchod,odpracovano FROM time WHERE prichod LIKE :prichod AND uzivatel=:user',
                        dict(prichod=od + '%', user=user))
                    return render_template('filter.html', root=True, row=row, filter=True, more=dotaz,
                                           celkem=database.openDatabase().celkem(dotaz))
                elif len(do) != 0:
                    dotaz = database.openDatabase().selectFilter(
                        'SELECT uzivatel,prichod,odchod,odpracovano FROM time WHERE odchod LIKE :odchod AND uzivatel=:user',
                        dict(odchod=do + '%', user=user))
                    return render_template('filter.html', root=True, row=row, filter=True, more=dotaz,
                                           celkem=database.openDatabase().celkem(dotaz))
                else:
                    dotaz = database.openDatabase().selectFilter(
                        'SELECT uzivatel,prichod,odchod,odpracovano FROM time WHERE uzivatel=:user', dict(user=user))
                    return render_template('filter.html', root=True, row=row, filter=True, more=dotaz,
                                           celkem=database.openDatabase().celkem(dotaz))
            except NameError:
                redirect('/filter')

        if request.form.get('submit') == 'Exportovat':
            return pdf.pdf(user, od, do)


@app.route('/oprava')
def oprava():
    row = database.openDatabase().selectUser()

    if row:
        return render_template('oprava.html', root=True, row=row, filter=True)
    else:
        return render_template('oprava.html', root=True)


@app.route('/oprava', methods=['GET', 'POST'])
def post_oprava():
    datum = request.form['date']
    user = request.form['jmeno']
    user = diakritika(user)
    row = database.openDatabase().selectUser()
    

    zaznamy = database.openDatabase().selectFilter(
        'SELECT id,prichod,odchod FROM time WHERE uzivatel =:user AND prichod like :prichod',
        dict(user=user, prichod=datum + "%"))
    global idZaznamu
 
    idZaznamu = zaznamy[0][0]
    
    if validace.Validovat(datum).isEmpty():
        return render_template('oprava.html', root=True, filter=True, oznaceni="red", row=row)


    if zaznamy:
        return render_template('oprava.html', root=True, filter=True, zaznamy=zaznamy, row=row, od=datum)
    else:
        return render_template('oprava.html', root=True, filter=True, zaznamy=False, row=row)

    if request.form.get('opravit') == 'oprava':
        heslo = request.form['heslo']
    prichod = request.form['prichod']
    dchod = request.form['odchod']
    overeni = overeniHesla.OverHeslo(heslo)
         
    
    if validace.isEmpty:
            return render_template('oprava.html', root=True, filter=True, error="red", row=row, zaznamy=zaznamy,od=datum)       

    elif overeni.over():
        import opravaCasu

        update = opravaCasu.OpravaDochazky(prichod, odchod, idZaznamu)
        # hodiny = database.openDatabase().pocetH(idZaznamu)
        update.doRepair()
        update.doRepairCas()
        if len(prichod) == 0 or len(odchod) == 0:
            return render_template('oprava.html', root=True, filter=True, error="red", row=row, zaznamy=zaznamy,
                                             od=datum, update=True, upd="Neprovedeno")
        return render_template('oprava.html', root=True, filter=True, error="red", row=row, zaznamy=zaznamy,
                                         od=datum, update=True, upd="Provedeno")
    else:
        return render_template('oprava.html', root=True, filter=True, error="red", row=row, zaznamy=zaznamy,
                                         od=datum, update=True, upd=u"Neplatné heslo")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
