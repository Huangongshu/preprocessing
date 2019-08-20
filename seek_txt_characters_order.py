# -*- coding: utf-8 -*-
#@author:huan 

import pandas as pd
from glob import glob
#from multiprocessing import Pool
#from functools import partial
import os
#import re


def judge_illness(string,patt): 
    '''
    Used to determine whether the label exists.
    parameter:
        string: the string you enter that needs to look for the pattern
        patt: the pattern,for exemple:'糖尿病'，'渗出血'
    '''
    t_eye='双眼'
    l_eye='左眼'
    r_eye='右眼'
    
    t_eye_str_order=string.find(t_eye) #Finding the order of pattern in a string
    l_eye_str_order=string.find(l_eye)
    r_eye_str_order=string.find(r_eye) 
    pat_str_order=string.find(patt)
    
    if pat_str_order !=-1: #pattern existence
        
        s_dict={t_eye:t_eye_str_order,l_eye:l_eye_str_order,r_eye:r_eye_str_order,patt:pat_str_order}
        order=dict(sorted(s_dict.items(),key=lambda x:x[1],reverse=False))
#        print(order)
        p_order=list(order).index(patt)    
        return list(order)[p_order-1] #return the eye_type
    
    else:
        
        return -1 #no illness


def matching_information(df,df1,i):
    test=judge_illness(df['影像诊断'][i],pattern)
#    print(test)
    
    if test=='双眼':
        df1=pd.concat([df1,pd.DataFrame({'挂号号码':[df.iloc[(i,0)]],'眼睛':\
            [df.iloc[(i,2)]],'期':[df.iloc[(i,11)]]})],axis=0,ignore_index=True)
    
    if (test=='左眼')&(df.iloc[(i,2)]=='左眼'):
        df1=pd.concat([df1,pd.DataFrame({'挂号号码':[df.iloc[(i,0)]],'眼睛':\
            [df.iloc[(i,2)]],'期':[df.iloc[(i,11)]]})],axis=0,ignore_index=True)
    
    if (test=='右眼')&(df.iloc[(i,2)]=='右眼'):
        df1=pd.concat([df1,pd.DataFrame({'挂号号码':[df.iloc[(i,0)]],'眼睛': \
             [df.iloc[(i,2)]],'期':[df.iloc[(i,11)]]})],axis=0,ignore_index=True)
    
    return df1


def take_out_data(df,source_col_name,value_str,eye_type_chinese_str):
    new_df=df[(df[source_col_name]==value_str)&(df['眼睛']==eye_type_chinese_str)]
    return new_df


def count_num(compared_path,df_dr_type_num,eye_type):
    count=0
    path_collection=[os.path.splitext(os.path.basename(x))[0].split('_')[0] for x in glob(compared_path+'/*.jpg') if os.path.splitext(os.path.basename(x))[0].split('_')[4]==eye_type]
    for num in df_dr_type_num['挂号号码']:
        if str(num) in path_collection:
            count+=1
    
    return count

def num_sum(df,im_path,type_num_str):
    l_1_df=take_out_data(df,'期',type_num_str,'左眼')
    r_1_df=take_out_data(df,'期',type_num_str,'右眼')
    l_1_num=count_num(im_path1,l_1_df,'L')
    r_1_num=count_num(im_path1,r_1_df,'R')
    return l_1_num+r_1_num

if __name__=='__main__':
    df=pd.read_excel('D:/第一和第二批2018和2019.xlsx')
    df['期']=df.影像诊断.str.extract('糖尿病视网膜病变[^0-9](\d)期',expand=False).fillna('0')
    df=df.drop(df.columns[0],axis=1)
    df1=pd.DataFrame(columns={'挂号号码','眼睛','期'})

    for i,n in zip(df.index,df['影像诊断']):
        if ('Ⅰ' in n) or ('糖尿病视网膜病变（非增殖，3期）' in n)or('糖尿病视网膜病变（非增殖，3期）' in n):
            df['期'][i]='1'
        elif ('Ⅱ'in n) or ('糖尿病视网膜病变2期' in n):
            df['期'][i]='2'
        elif ('Ⅲ' in n) or ('糖尿病视网膜病变（非增殖，3期）' in n):
            df['期'][i]='3'
        elif 'Ⅳ' in n:
            df['期'][i]='4'
        elif 'Ⅴ' in n:
            df['期'][i]='5'
        elif 'Ⅵ' in n:
            df['期'][i]='6'             

    pattern='糖尿病视网膜病变'

    for i in range(len(df)):
        df1=matching_information(df,df1,i)

    im_path1='D:/huan/第二批数据过滤/abnormal2'
    im_path2='D:/huan/第二批数据过滤/normal2'

    type_1_num=num_sum(df1,im_path1,'1')+num_sum(df1,im_path2,'1')
    type_2_num=num_sum(df1,im_path1,'2')+num_sum(df1,im_path2,'2')
    type_3_num=num_sum(df1,im_path1,'3')+num_sum(df1,im_path2,'3')
    type_4_num=num_sum(df1,im_path1,'4')+num_sum(df1,im_path2,'4')
    type_5_num=num_sum(df1,im_path1,'5')+num_sum(df1,im_path2,'5')
    type_6_num=num_sum(df1,im_path1,'6')+num_sum(df1,im_path2,'6')

    sum_num=type_1_num+type_2_num+type_3_num+type_4_num+type_5_num+type_6_num
