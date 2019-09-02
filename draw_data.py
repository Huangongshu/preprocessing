# -*- coding: utf-8 -*-
#@author:huan

import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
import os


def get_train_data(path):
    file_path=glob(path+'/*.txt')
    n=[]
    loss=[]
    accuracy=[]
    for p in file_path:
        n=int(os.path.basename(p).split('_')[3].split('.')[0])
        with open(p,'r') as f:
            d=f.read().split('-')
            loss.append([n,float(d[0])])
            accuracy.append([n,float(d[3])])
    loss=sorted(loss,key=(lambda x:x[0]),reverse=False)
    loss=[y for x,y in loss]
    accuracy=sorted(accuracy,key=(lambda x:x[0]),reverse=False)
    accuracy=[y for x,y in accuracy]    
    return loss,accuracy


def get_data(path,num):
    file_path=glob(path+'/*.xlsx')
    acc=[]
    sensitivity=[]
    specificity=[]    
    for p in file_path:
        n=int(os.path.basename(p).split('d')[num].split('.')[0])
        d=pd.read_excel(p)
        acc.append([n,d.iloc[0,1]])
        sensitivity.append([n,d.iloc[0,4]])
        specificity.append([n,d.iloc[0,5]]) 
    acc=sorted(acc,key=(lambda x:x[0]),reverse=False)  
    acc=[y for x,y in acc]     
    sensitivity=sorted(sensitivity,key=(lambda x:x[0]),reverse=False)
    sensitivity=[y for x,y in sensitivity]
    specificity=sorted(specificity,key=(lambda x:x[0]),reverse=False)        
    specificity=[y for x,y in specificity]
    return acc,sensitivity,specificity

name='resnet'
train_path='C:/Users/27011/Desktop/'+name+'_train'
train_loss,train_accuracy=get_train_data(train_path)

test_path='C:/Users/27011/Desktop/'+name+'_test'
test_acc,test_sensitivity,test_specificity=get_data(test_path,1)

validation_path='C:/Users/27011/Desktop/'+name+'_validation'
va_acc,va_sensitivity,va_specificity=get_data(validation_path,2)


plt.figure(0,figsize=(14,8))
plt.title('train_loss')
plt.plot(train_loss,label='train_loss',color='red')

plt.figure(1,figsize=(14,8))
plt.title('accuracy')
plt.plot(train_accuracy,label='train_loss',color='black')
plt.plot(test_acc,label='test_acc',color='green')
plt.plot(va_acc,label='va_acc',color='red')

plt.figure(2,figsize=(14,8))
plt.title('test')
plt.plot(test_specificity,label='test_specificity',color='red')
plt.plot(test_sensitivity,label='test_sensitivity',color='green')

plt.figure(3,figsize=(14,8))
plt.title('validation')
plt.plot(va_sensitivity,label='va_sensitivity',color='yellow')
plt.plot(va_specificity,label='va_specificity',color='gray')
plt.show()
