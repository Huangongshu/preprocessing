# -*- coding: utf-8 -*-
#@author:huan

from glob import glob
import pandas as pd
import os

#class Make_label():
#    def __init__(self,im_path,im_type,label_excel_path,list_label_rank):
#        self.im_path=im_path
#        self.im_type=im_type
#        self.label_excel_path=label_excel_path
#        self.label_df=None
#        self.read_excel()
#        self.read_im_path()
#    
#    def read_excel(self):
#        self.excel_df=pd.read_excel(self.label_excel_path)
#        
#     
#    def read_im_path(self):
#        self.im_path_lis=[x for x in glob(self.im_path+'/*.'+self.im_type)]
            
        
#    def make_im_label(self):
#        for num,path_name in enumerate(self.im_path_df[self.im_path_df.columns[0]]):
#            split_lis=os.path.basename(path_name).split('_')
#            if split_lis[4]=='L':
#                self.label_df=pd.concat([self.im_path_df.iloc[num],self.excel_df[(self.excel_df['挂号号码']==split_lis[0])&(self.excel_df['眼睛']=='左眼')]],axis=1,ignore_index=True)
# 
#            if split_lis[4]=='L':
#                self.label_df=pd.concat([self.im_path_df.iloc[num],self.excel_df[(self.excel_df['挂号号码']==split_lis[0])&(self.excel_df['眼睛']=='右眼')]],axis=1,ignore_index=True)    

 
im_path=r'D:/huan/new_high_res_merge/blur'
label_excel_path='D:/第一和第二批2018和2019.xlsx'
im_type='jpg'
excel_df=pd.read_excel(label_excel_path)
im_path_lis=[x for x in glob(im_path+'/*.'+'jpg')]
#im_path_df=pd.DataFrame(im_path_lis)
#m=Make_label(im_path,im_type,label_excel_path,[3,4,5])
#m.make_im_label()

l=[]
label_df=pd.DataFrame()

for num,path in enumerate(im_path_lis):
    split_lis=os.path.basename(path).split('_')
    if split_lis[4]=='L':    
        tem=excel_df[(excel_df['挂号号码']==int(split_lis[0]))&(excel_df['眼睛']=='左眼')]
        if len(tem)!=0:
            s=path+' '+str(tem.iloc[0,4])+' '+str(tem.iloc[0,5])+' '+str(tem.iloc[0,6])+' '+str(tem.iloc[0,7])+' '+str(tem.iloc[0,8])+' '+str(tem.iloc[0,9])
            l.append(s)
    elif split_lis[4]=='R':
        tem=excel_df[(excel_df['挂号号码']==int(split_lis[0]))&(excel_df['眼睛']=='右眼')]
        if len(tem)!=0:
            s=path+' '+str(tem.iloc[0,4])+' '+str(tem.iloc[0,5])+' '+str(tem.iloc[0,6])+' '+str(tem.iloc[0,7])+' '+str(tem.iloc[0,8])+' '+str(tem.iloc[0,9])
            l.append(s)  
            
with open('make_label.txt','w') as f:
    for i in l:
        f.writelines(str(i)+'\n')
        
#import cv2 
# 
#im=cv2.imread(l[0].split()[0])
#cv2.imshow('',im)
#cv2.waitKey(100)
