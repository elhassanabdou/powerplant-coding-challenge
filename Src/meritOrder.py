#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 18:43:34 2021

@author: elhassan
"""
import uvicorn
from typing import List, Optional, Dict
from fastapi import FastAPI

#from fastapi.testclient import TestClient
#from pydantic import BaseModel
import numpy as np
from scipy.optimize import linprog

def constructLPParameters(item:Dict):
    l = item["powerplants"]
    f = item["fuels"]
    lb = []
    ub=[]
    Aeq = np.ones((1,len(l)))
    beq = np.ndarray(1)
    beq[0]=item["load"]
    C = np.zeros(len(l))
    counter = 0;
    
    for x in l:
        lb.append(x["pmin"])
        ub.append(x["pmax"])
        if(x["type"]=="turbojet"):
            C[counter]=(1-x["efficiency"])*f['gas(euro/MWh)']
        elif(x["type"]=="gasfired"):
            C[counter]=(1-x["efficiency"])*f['kerosine(euro/MWh)']
        elif(x["type"]=="windturbine"):
            ub[-1] = ub[-1]*(f["wind(%)"]/100)
            C[counter]=-1
        counter = counter+1
    bounds = np.array([lb,ub])
    bounds = np.transpose(bounds)
    return C,Aeq,beq,bounds
    
    
        
app = FastAPI()

@app.post("/items/")
async def calMeritOrder(item:Dict):
    C,Aeq,beq,bounds = constructLPParameters(item)
    #call function of the linear programming here
    res = linprog(c= C,A_eq =Aeq,b_eq=beq,bounds=bounds)
    resultdic={}
    l = item["powerplants"]
    for ll in range(len(res.x)):
        powername = l[ll]["name"]
        resultdic[powername]=res.x[ll]
    return resultdic 

    
        
if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8888)