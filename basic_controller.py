# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 15:48:33 2017

@author: rohan
"""
from flask import Flask
import os
import numpy as np
import pandas as pd
from bson import json_util
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    

@app.route("/read/bills/<mkt_type>")
def read_bills(mkt_type):
        
    bill_loc="/home/rohan/papas_app/n019/bills/"
    reading_pickle = pd.read_pickle(bill_loc+mkt_type+".pickle")
    x=""
    x+=str(reading_pickle[0][0])
    x+="</br><table border='1'>"    
    for i in reading_pickle[1:]:
        x+="<tr>"
        for j in i:

            x+="<td>"
            x+=str(j)
            x+="</td>"
            
        x+="</tr>"
    x+="<table>"
    
    return x
    
@app.route("/read/ledger/<client_code>")
def read_ledger(client_code):
    x = ""
    #bill_loc="/home/rohan/papas_app/ledger/"+client_code+".pickle"
    ledger_read = pd.read_pickle("/home/rohan/papas_app/ledger/"+client_code+".pickle")    
    ledger_head = pd.read_pickle("/home/rohan/papas_app/ledger/headers.pickle")
    x += (ledger_read[0][0]+"</br>")    
    x += (ledger_read[1][0]+"</br>")
    x +="<table border='1'>"
    x +="<tr>"
    for i in range(0,len(ledger_head)):
        x+=("<th>"+str(ledger_head[i])+"</th>")
    x+="</tr>"
    
    for j in range(2,len(ledger_read)):
        x+="<tr>"
        for k in ledger_read[j]:
            x+=("<td>"+str(k)+"</td>")
    
        x+="</tr>"
        
    x+="</table>"
    
    return x
    
@app.route("/view/static")
def static_temp():
    return render_template("login.html")
    
    
@app.route("/read/json/ledger/<client_code>")
def read_json_ledger(client_code):
    ledger_read = pd.read_pickle("/home/rohan/papas_app/ledger/"+client_code+".pickle")    
    ledger_head = pd.read_pickle("/home/rohan/papas_app/ledger/headers.pickle")
    lis =[]
    lis.append({
        "NAME":ledger_read[0][0],
        "COMPANY":ledger_read[1][0]    
    })
    for i in range(2,len(ledger_read)):
        dic={}    
        for j in range(0,len(ledger_read[i])):
           dic[ledger_head[j]]=ledger_read[i][j]
        
        lis.append(dic)
        
    return json.dumps(lis,default=json_util.default)
    
if __name__ == '__main__':
   app.run(debug = True)