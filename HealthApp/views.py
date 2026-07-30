from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import pymysql
import pyaes, pbkdf2, binascii, os, secrets, base64

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AccessIOT(request):
    if request.method == 'GET':
       return render(request, 'AccessIOT.html', {})     

#decrypt file using AES
def AESdecrypt(enc): 
    aes = pyaes.AESModeOfOperationCTR("abcd5643abcd5643abcd5643abcd5643".encode(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

def AccessIOTAction(request):
    if request.method == 'POST':
        iot = request.POST.get('t1', False)
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Patient IOT ID</th>'
        output+='<th><font size="3" color="black">Heart Rate</th><th><font size="3" color="black">Temperature</th>'
        output+='<th><font size="3" color="black">BP Systolic</th><th><font size="3" color="black">BP Diastolic</th>'
        output+='<th><font size="3" color="black">AI Health Prediction</th><th><font size="3" color="black">Recorded Date</th></tr>'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'smarthealth',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from patientdata where patient_id='"+iot+"'")
            rows = cur.fetchall()
            for row in rows:
                hr = AESdecrypt(base64.b64decode(row[1])).decode()
                temp = AESdecrypt(base64.b64decode(row[2])).decode()
                sis = AESdecrypt(base64.b64decode(row[3])).decode()
                dis = AESdecrypt(base64.b64decode(row[4])).decode()
                output+='<tr><td><font size="3" color="black">'+str(row[0])+'</td>'
                output += '<td><font size="3" color="black">'+hr+'</td>'
                output += '<td><font size="3" color="black">'+temp+'</td>'
                output += '<td><font size="3" color="black">'+sis+'</td>'
                output += '<td><font size="3" color="black">'+dis+'</td>'
                output += '<td><font size="3" color="black">'+row[5]+'</td>'
                output += '<td><font size="3" color="black">'+row[6]+'</td></tr>'
        output+= "</table></br></br></br></br>" 
        context= {'data':output}
        return render(request, 'index.html', context)       
        
    
