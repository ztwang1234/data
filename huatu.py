# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:51:53 2018

@author: wangz
"""

import numpy as np
import matplotlib.pyplot as plt
import visa
import time


rm=visa.ResourceManager()
pna=rm.open_resource('TCPIP::10.122.7.250')
pna.timeout = 10000

#currentR=rm.open_resource('TCPIP::10.122.7.201')

def get_S(pna):
    quote = '" '
    msg = pna.query('CALC%d:PAR:CAT?' % 1).strip(quote)
    measname = msg.split(',')[0]
    pna.write('CALC%d:PAR:SEL "%s"' % (1, measname))
    
    pna.write('INIT:CONT OFF')
    pna.write('INIT:IMM')
    pna.write('*WAI')
    time.sleep(1)
    pna.write('FORMAT:BORD NORM')
    pna.write('FORMAT ASCII')
    
    cmd = "CALC1:DATA? SDATA"
    
    data = np.asarray(pna.query_ascii_values(cmd))
    data = data[::2]+1j*data[1::2]
    pna.write('INIT:CONT ON')
    return data

def get_freq(pna):
    quote = '" '
    msg = pna.query('CALC%d:PAR:CAT?' % 1).strip(quote)
    measname = msg.split(',')[0]
    pna.write('CALC%d:PAR:SEL "%s"' % (1, measname))
    
    cmd = 'CALC:X?'
    return np.asarray(pna.query_ascii_values(cmd))

def set_power(pna):

    
    pna.write('SOUR:POW1 %s' %str(i))
   
    cmd='SOUR:POW?'
    #print(np.asarray(inst.query_ascii_values(cmd)))
    return np.asarray(pna.query_ascii_values(cmd))


power=[]
S=[]
freq=get_freq(pna)
for i in range(-15,5):    
    set_power(pna)
    get_freq(pna)  
    
    power.append(i)
    S.append(np.abs(get_S(pna)))
   
plt.imshow(S,aspect='auto',interpolation='nearest', extent=(min(freq),max(freq),min(power),max(power)))   
plt.show()  

plt.savefig(datetime.now().date().strftime('%Y%m%d')+'.jpg')

def txt_save(data, i):
    data=data.tolist()
    file = open(datetime.now().date().strftime('%Y%m%d')+'.txt', 'a')
    file.write(i+'\n')
    for i in range(len(data)):    
        s = str(data[i]).replace('[','').replace(']','') 
        s = s.replace("'",'').replace(',','')+'\n'    
        file.write(s)
    file.close()        
    print("保存文件成功") 

txt_save(S,'S')
txt_save(freq,'freq')
txt_save(power,'power')