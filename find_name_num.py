# -*- coding: utf-8 -*-
#autor:huan

import pandas as pd

def cal_name(df):
    a=[]
    for i in range(len(df)): 
        count = 0
        for na in name:
            if na in df.iloc[i, 2]:
                count += 1
        if count > 1:
            a.append(i)
    df.iloc[a].to_csv('C:/Users/huan/Documents/WeChat Files/wxid_qxjqyd4y9ft721/Files/train(1)/result.csv')

if __name__=='__main__':
    df=pd.read_csv('C:/Users/huan/Documents/WeChat Files/wxid_qxjqyd4y9ft721/Files/train(1)/train.csv')
    name=['Cardiomegaly','Hernia','Infiltration','Pleural_Thickening','Fibrosis',\
          'Effusion','Mass','Nodule','Pneumothorax','Atelectasis','Pneumonia',\
          'Emphysema','Edema','Consolidation']
    cal_name(df)
