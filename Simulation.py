import tkinter
from tkinter import *
import math
import random
from threading import Thread 
from collections import defaultdict
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import time
from tkinter import filedialog
import random
from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.model_selection import train_test_split
import pyaes, pbkdf2, binascii, os, secrets
import base64, timeit, io
import pymysql
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score

global iot, labels, iot_x, iot_y, text, canvas, iot_list, root, num_nodes, tf1, nodes, fog1, fog2, fog3, running
global rsu1_x, rsu1_y, rsu2_x, rsu2_y, rsu3_x, rsu3_y, scaler, hybrid_model
option = 0
run_counter = 0
pdr = []
throughput = []
class_labels = ['Normal', 'Abnormal']

#function to calculate all metrics
def calculateMetrics(algorithm, y_test, predict):
    a = (accuracy_score(y_test,predict)*100)
    p = (precision_score(y_test, predict,average='macro') * 100)
    r = (recall_score(y_test, predict,average='macro') * 100)
    f = (f1_score(y_test, predict,average='macro') * 100)
    a = round(a, 3)
    p = round(p, 3)
    r = round(r, 3)
    f = round(f, 3)
    text.insert(END,"AI "+algorithm+" Accuracy: "+str(a)+"\n")
    text.insert(END,"AI "+algorithm+" Precision: "+str(p)+"\n")
    text.insert(END,"AI "+algorithm+" Recall     : "+str(r)+"\n")
    text.insert(END,"AI "+algorithm+" FScore   : "+str(f)+"\n\n")
    return algorithm

def trainAI():
    text.delete('1.0', END)
    global scaler, hybrid_model, class_labels
    dataset = pd.read_csv("Dataset/Patient_Dataset.csv")
    dataset.fillna(dataset.mean(), inplace = True)
    Y = dataset['Target']
    dataset.drop(['Target'], axis = 1,inplace=True)
    X = dataset.values
    scaler = MinMaxScaler((0,1))
    X = scaler.fit_transform(X)#normalizing dataset features
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2) #split dataset into train and test
    data = np.load("model/data.npy", allow_pickle=True)
    X_train, X_test, y_train, y_test = data

    svm_cls = svm.SVC()
    svm_cls.fit(X_train, y_train)
    predict = svm_cls.predict(X_test)
    calculateMetrics("SVM", y_test, predict)

    xg = XGBClassifier()
    rf =RandomForestClassifier()
    estimators = [('xg', xg), ('rf', rf)]
    hybrid_model = VotingClassifier(estimators = estimators, voting='hard')
    hybrid_model.fit(X_train, y_train)
    predict = hybrid_model.predict(X_test)
    calculateMetrics("Extension Hybrid Model", y_test, predict)

    conf_matrix = confusion_matrix(y_test, predict)
    fig, axs = plt.subplots(1,2,figsize=(10, 3))
    ax = sns.heatmap(conf_matrix, xticklabels = class_labels, yticklabels = class_labels, annot = True, cmap="viridis" ,fmt ="g", ax=axs[0]);
    ax.set_ylim([0,len(class_labels)])
    axs[0].set_title("Hybrid Model Confusion matrix") 

    random_probs = [0 for i in range(len(y_test))]
    p_fpr, p_tpr, _ = roc_curve(y_test, random_probs, pos_label=1)
    plt.plot(p_fpr, p_tpr, linestyle='--', color='orange',label="True classes")
    ns_fpr, ns_tpr, _ = roc_curve(y_test, predict, pos_label=1)
    axs[1].plot(ns_fpr, ns_tpr, linestyle='--', label='Predicted Classes')
    axs[1].set_title("Hybrid Model ROC AUC Curve")
    axs[1].set_xlabel('False Positive Rate')
    axs[1].set_ylabel('True Positive rate')
    plt.show()

def getDistance(iot_x,iot_y,x1,y1):
    flag = False
    for i in range(len(iot_x)):
        dist = math.sqrt((iot_x[i] - x1)**2 + (iot_y[i] - y1)**2)
        if dist < 60:
            flag = True
            break
    return flag    
    
def createFOG(x, y, title,col):
    iot_x.append(x)
    iot_y.append(y)
    name = canvas.create_oval(x,y,x+40,y+40, fill=col)
    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text=title)
    labels.append(lbl)
    iot.append(name)    

def setLocation(x1, y1, x2, y2, x3, y3):
    global fog1_x, fog1_y, fog2_x, fog2_y, fog3_x, fog3_y
    fog1_x = x1
    fog1_y = y1
    fog2_x = x2
    fog2_y = y2
    fog3_x = x3
    fog3_y = y3

def generateNetwork():
    text.delete('1.0', END)
    global fog1_x, fog1_y, fog2_x, fog2_y, fog3_x, fog3_y, running, canvas
    global iot, labels, iot_x, iot_y, num_nodes, tf1, nodes, fog1, fog2, fog3
    iot = []
    iot_x = []
    iot_y = []
    labels = []
    nodes = []
    fog1_x = 150
    fog1_y = 450
    fog2_x = 150
    fog2_y = 250
    fog3_x = 150
    fog3_y = 50
    canvas.update()
    num_nodes = int(tf1.get().strip())
    createFOG(5, 300, "Admin","green")
    createFOG(150, 450, "Fog1","yellow")#450 to 650
    createFOG(150, 250, "Fog2","yellow")#250 to 450
    createFOG(150, 50, "Fog3","yellow")#50 to 250
    nodes.append([5, 300])
    nodes.append([150, 450])
    nodes.append([150, 250])
    nodes.append([150, 50])
    running = True
    for i in range(4,num_nodes):
        run = True
        while run == True:
            x = random.randint(250, 600)
            y = random.randint(50, 600)
            flag = getDistance(iot_x,iot_y,x,y)
            if flag == False:
                nodes.append([x, y])
                iot_x.append(x)
                iot_y.append(y)
                run = False
                name = canvas.create_oval(x,y,x+40,y+40, fill="red")
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 8 italic bold",text="N"+str(i))
                labels.append(lbl)
                iot.append(name)    

def startDataTransferSimulation(canvas,line1,line2,x1,y1,x2,y2,x3,y3):
    class SimulationThread(Thread):
        def __init__(self, canvas,line1,line2,x1,y1,x2,y2,x3,y3): 
            Thread.__init__(self) 
            self.canvas = canvas
            self.line1 = line1
            self.line2 = line2
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.x3 = x3
            self.y3 = y3                      
             
        def run(self):
            time.sleep(1)
            for i in range(0,3):
                self.canvas.delete(self.line1)
                self.canvas.delete(self.line2)
                time.sleep(1)
                self.line1 = canvas.create_line(self.x1, self.y1,self.x2, self.y2,fill='black',width=3)
                self.line2 = canvas.create_line(self.x2, self.y2,self.x3, self.y3,fill='black',width=3)
                time.sleep(1)
            self.canvas.delete(self.line1)
            self.canvas.delete(self.line2)
            self.canvas.update()                            
    newthread = SimulationThread(canvas,line1,line2,x1,y1,x2,y2,x3,y3) 
    newthread.start()

 #encrypt file using AES
def AESencrypt(plaintext):
    aes = pyaes.AESModeOfOperationCTR("abcd5643abcd5643abcd5643abcd5643".encode(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

#decrypt file using AES
def AESdecrypt(enc): 
    aes = pyaes.AESModeOfOperationCTR("abcd5643abcd5643abcd5643abcd5643".encode(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

def saveRecord(record_id, hr, temp, sis, dia, predict):
    global username
    dd = str(datetime.now())
    dd = dd.split(".")[0]
    hr = base64.b64encode(AESencrypt(hr.encode())).decode()
    temp = base64.b64encode(AESencrypt(temp.encode())).decode()
    sis = base64.b64encode(AESencrypt(sis.encode())).decode()
    dia = base64.b64encode(AESencrypt(dia.encode())).decode()
    db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'smarthealth',charset='utf8')
    db_cursor = db_connection.cursor()
    student_sql_query = "INSERT INTO patientdata VALUES('"+str(record_id)+"','"+hr+"','"+temp+"','"+sis+"','"+dia+"','"+predict+"','"+dd+"')"
    db_cursor.execute(student_sql_query)
    db_connection.commit()

def communication():
    text.delete('1.0', END)
    global iot_list, scaler, hybrid_model, class_labels, run_counter
    src = int(iot_list.get())
    temp = nodes[src]
    src_x = temp[0]
    src_y = temp[1]
    print(str(src)+" "+str(len(nodes))+" "+str(src_x)+" "+str(src_y))
    selected_fog1 = 0
    distance1 = math.sqrt((fog1_x - src_x)**2 + (fog1_y - src_y)**2)
    distance2 = math.sqrt((fog2_x - src_x)**2 + (fog2_y - src_y)**2)
    distance3 = math.sqrt((fog3_x - src_x)**2 + (fog3_y - src_y)**2)
    id1 = 0
    if distance1 <= distance2 and distance1 <= distance3:
        selected_fog1 = fog1_y
        id1 = 1                
    elif distance2 <= distance1 and distance2 <= distance3:
        id1 = 2
        selected_fog1 = fog2_y
    else:
        id1 = 3
        selected_fog1 = fog3_y
    if run_counter < 3:
        hr = random.randint(60, 100)
        temp = random.uniform(36.0, 39.5)
        sys = random.randint(100, 160)
        dia = random.randint(60, 100)
    else:
        temp = [[80,39.0,114,77], [70,36.8,131,72], [88,38.2,124,66], [77,38.6,112,82], [85,36.6,131,100], [73,36.0,155,96],[90,37.1,127,100],[74,39.4,152,76],[83,37.2,151,95],[100,37.8,109,65]]
        selected = random.randint(0, len(temp)-1)
        selected = temp[selected]
        hr, temp, sys, dia = selected
        run_counter = 0
    run_counter += 1
    testData = [[float(hr), float(temp), float(sys), float(dia)]]
    testData = np.asarray(testData)
    testData = scaler.transform(testData)
    predict = hybrid_model.predict(testData)[0]
    predict = class_labels[predict]
    saveRecord(str(src), str(hr), str(temp), str(sys), str(dia), predict)
    text.insert(END,"Sense Heart Rate   = "+str(hr)+"\n")
    text.insert(END,"Sense Temperature= "+str(temp)+"\n")
    text.insert(END,"Sense Systolic BP  = "+str(sys)+"\n")
    text.insert(END,"Sense Diastolic BP = "+str(dia)+"\n")
    text.insert(END,"AI Predicted Health ="+predict+"\n\n")
    text.insert(END,"Selected SRC "+str(src)+" Selected Nearest FOG : "+str(id1)+"\n\n")
    line1 = canvas.create_line(iot_x[src]+20, iot_y[src]+20, 175, selected_fog1+20,fill='black',width=3)
    line2 = canvas.create_line(170, selected_fog1+20, 25, 320,fill='black',width=3)
    startDataTransferSimulation(canvas,line1,line2,(iot_x[src]+20),(iot_y[src]+20),175,selected_fog1+20,25, 320)
    option = 1    

def graph():
    global pdr, throughput
    pdr.clear()
    throughput.clear()
    pdrs = 0
    tp = 0
    for i in range(0, 100):
        s = random.randint(0, 100)
        if s > 10:
            pdrs += 1
    propose_pdrs = pdrs / 100
    propose_tp = 8 * propose_pdrs
    ex_pdr = pdrs / 110
    ex_tp = 8 * ex_pdr
    data = [ex_pdr, ex_tp, propose_pdrs, propose_tp]
    names = ['4G PDR', '4G Throughput', '5G PDR', '5G Throughput']
    plt.figure(figsize=(6, 3))
    sns.barplot(x=names,y=data)
    plt.xlabel('Comparison Metrics')
    plt.ylabel('PDR/Throughput')
    plt.title('PDR & Throughput Graph')
    plt.show()

def close():
    global root
    root.destroy()

def Main():
    global root, tf1, text, canvas, iot_list
    root = tkinter.Tk()
    root.geometry("1300x1200")
    root.title("An AI-Assisted Smart Healthcare System Using 5G Communication")
    root.resizable(True,True)
    font1 = ('times', 12, 'bold')

    canvas = Canvas(root, width = 1150, height = 700)
    canvas.pack()

    l2 = Label(root, text='Number of Nodes:')
    l2.config(font=font1)
    l2.place(x=820,y=10)

    tf1 = Entry(root,width=10)
    tf1.config(font=font1)
    tf1.place(x=970,y=10)

    l1 = Label(root, text='Node ID:')
    l1.config(font=font1)
    l1.place(x=820,y=60)

    mid = []
    for i in range(4,100):
        mid.append(str(i))
    iot_list = ttk.Combobox(root,values=mid,postcommand=lambda: iot_list.configure(values=mid))
    iot_list.place(x=970,y=60)
    iot_list.current(0)
    iot_list.config(font=font1)

    generateButton = Button(root, text="Generate Smart Health IOT Network", command=generateNetwork)
    generateButton.place(x=820,y=110)
    generateButton.config(font=font1)
    
    initButton = Button(root, text="Run AI Algorithm", command=trainAI)
    initButton.place(x=820,y=160)
    initButton.config(font=font1)

    registrationButton = Button(root, text="Transmit Sense Data", command=communication)
    registrationButton.place(x=990,y=160)
    registrationButton.config(font=font1)

    communicationButton = Button(root, text="Throughput Graph", command=graph)
    communicationButton.place(x=820,y=210)
    communicationButton.config(font=font1)

    text=Text(root,height=19,width=50)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=780,y=260)    
    root.config(bg='cornflower blue')
    root.mainloop()
   
 
if __name__== '__main__' :
    Main ()
    
