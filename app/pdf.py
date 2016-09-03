# -*- coding: utf-8 -*-
from flask import make_response, redirect, Response
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import black, red, green, navy, white, blue, grey, yellow, pink, orange, lavender
import rl_config
from reportlab.lib.units import inch
from reportlab.platypus import Image, SimpleDocTemplate, Spacer, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


def Data(od,do):
    import database
    dotaz = database.openDatabase().selectFilter('SELECT prichod,odchod,odpracovano FROM time WHERE prichod BETWEEN :prichod AND :odchod', dict(prichod=od,odchod=do))			
    return dotaz

def savePdf(filename):
    '''
    import getOs
    getOsName = getOs.os()
    path = getOsName.changeDir(getOsName.osWindows())
    '''
    path = '/home/p9poslt/Dokumenty/'
    outfilename = filename
    outfilepath = os.path.join(path,outfilename)
    doc = SimpleDocTemplate(outfilepath)


def pdf(name,od,do):
    getName = '-'.join([name,od,do])+'.pdf'
    doc = SimpleDocTemplate(getName)
    pdfmetrics.registerFont(TTFont('FreeMono', 'FreeMono.ttf'))
    styles = getSampleStyleSheet()
    Story = [Spacer(1,1)]
    hlavicka = u'Export docházky'
    
    headtext = ParagraphStyle('mystyle',
                              fontName='FreeMono',
                              fontSize=18,
                              textColor=red,
                              spaceAfter=12,
                              alignment = TA_CENTER)
    
    p = Paragraph(hlavicka,headtext)
    Story.append(p)
    
    info = name + ' ' + od + ' ' + do
    infotext = ParagraphStyle('info',
                              fontName='FreeMono',
                              fontSize= 10,
                              textColor=blue,
                              spaceAfter=30,
                              alignment=TA_CENTER)
    p = Paragraph(info,infotext)
    Story.append(p)
    

    
    data=[]
    dotaz = Data(od,do)
    for col in dotaz:
        data.append(col)
        
    t=Table(data,style=[
    ('GRID',(0,0),(-1,-1),0.5,grey),
    ('BOX',(3,0),(1,-1),1,red),
    ('BOX',(0,0),(-1,-1),2,black),
    ('BACKGROUND',(0,0),(-1,-1),lavender)
    ])    
        
    Story.append(t)
    celkemH = ParagraphStyle('celkem',
                            fontName='FreeMono',
                            fontSize= 10,
                            textColor=red,                           
                            alignment=TA_CENTER)
    def celkem(hodiny):
        hodin = 0
        minut = 0
        if hodiny:
            for i in hodiny:
                if i[2] !=None:
                    hodin +=int(i[2][:2])
                    minut +=int(i[2][3:])
                    if minut > 60:
                        minut = minut - 60
                        hodin = hodin+1
            result = str(hodin)+":"+str(minut)
            return result
        else:
            return False
    p= Paragraph('Odpracováno celkem '+ celkem(data)+' hodin',celkemH)
    Story.append(p)
    
    podpis =  ParagraphStyle('podpis',
                              fontName='FreeMono',
                              fontSize= 10,
                              textColor=blue,
                              spaceBefore =50,
                              spaceAfter=0,
                              alignment=TA_RIGHT)
    p = Paragraph('-------------------------',podpis)
    Story.append(p)
    
    podpisZ =  ParagraphStyle('podpisZ',
                                  fontName='FreeMono',
                                  fontSize= 10,
                                  textColor=blue,
                                  spaceBefore =0,
                                  spaceAfter=30,
                                  alignment=TA_RIGHT)
    p = Paragraph('podpis zaměstnance',podpisZ)
    Story.append(p)    
    
    
    #savePdf(Story)
    doc.build(Story)
    
    
    #open file
    #import webbrowser
    #open = webbrowser.open(getName)
    #headers=["Content-Disposition"] = "attachment; filename=getName"
    response = Response(mimetype='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename=getName'  
    
    #return make_response((headers))
    
    return redirect('/filter')



