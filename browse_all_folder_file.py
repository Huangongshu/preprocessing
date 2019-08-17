# -*- coding: utf-8 -*-
#@author:huan

import os
from glob import glob
import shutil as sh
import pandas as pd
from check_inperfect_image import CheckImage

def handle_image_data(base_path,number_list,save_image_path,eye_type):
    '''
    parameter:
        base_path: The home folder path of the picture
        number_list: The corresponding of the number list
        eye_type:'L' or 'R'
    '''
    for base_name,sub_dirname,filename in os.walk(base_path):
        for sub_path in sub_dirname:
            for i in glob(os.path.join(base_path,sub_path)+'/*.jpg'):
                sp_list=os.path.basename(i).split('_')
                if int(sp_list[0]) in number_list and sp_list[4]==eye_type:#When applied, it should be modified according to the number and eye type.
                    try:
                        c=CheckImage(i)
                        if c.check_jpg_jpeg():
                            if c.check_im_size():
                                sh.copy(i,save_image_path)
                    except OSError:
                        print('出现异常文件,路径为：',i)

def statistic_image_data(base_path,number_list,eye_type):
    '''
    parameter:
        base_path: The home folder path of the picture
        number_list: The corresponding of the number list
        eye_type:'L' or 'R'
    '''
    count=0
    for base_name,sub_dirname,filename in os.walk(base_path):
        for sub_path in sub_dirname:
            for i in glob(os.path.join(base_path,sub_path)+'/*.jpg'):
                sp_list=os.path.basename(i).split('_')
                if int(sp_list[0]) in number_list and sp_list[4]==eye_type:#When applied, it should be modified according to the number and eye type.
                    count=count+1
    return count

if __name__=='__main__': 
    
    #all path

    base_path=r'D:/huan/视眼膜眼底筛查------20190730/糖网眼底图第二批'
    label_path='D:/huan/视眼膜眼底筛查------20190730/眼底筛查AI标签第二批(5).xlsx'
    no_illness_normal_image_copy_path='D:/huan/视眼膜眼底筛查------20190730/DR_data/no_illness_normal2/'
    illness_normal_image_copy_path='D:/huan/视眼膜眼底筛查------20190730/DR_data/illness_normal2/'    
    no_normal_image_copy_path='d:/huan/视眼膜眼底筛查------20190730/DR_data/abnormal2/'

    #提取匹配信息
    df = pd.read_excel(label_path)  
    illness_left_normal_list=list(df[(df.图像不清晰!=1) & (df.眼睛=='左眼')&(df.糖尿病视网膜病变==1)]['挂号号码'])
    illness_right_normal_list=list(df[(df.图像不清晰!=1) & (df.眼睛=='右眼')&(df.糖尿病视网膜病变==1)]['挂号号码'])  
    no_illness_left_normal_list=list(df[(df.图像不清晰!=1) & (df.眼睛=='左眼')&(df.糖尿病视网膜病变==0)]['挂号号码'])    
    no_illness_right_normal_list=list(df[(df.图像不清晰!=1) & (df.眼睛=='右眼')&(df.糖尿病视网膜病变==0)]['挂号号码'])     
    no_left_normal_list=list(df[(df.图像不清晰==1) & (df.眼睛=='左眼')]['挂号号码']) 
    no_right_normal_list=list(df[(df.图像不清晰==1) & (df.眼睛=='右眼')]['挂号号码'])
             
    handle_image_data(base_path,illness_left_normal_list,illness_normal_image_copy_path,'L') 
    handle_image_data(base_path,illness_right_normal_list,illness_normal_image_copy_path,'R')
    handle_image_data(base_path,no_illness_left_normal_list,no_illness_normal_image_copy_path,'L')
    handle_image_data(base_path,no_illness_right_normal_list,no_illness_normal_image_copy_path,'R')    
    handle_image_data(base_path,no_left_normal_list,no_normal_image_copy_path,'L')
    handle_image_data(base_path,no_right_normal_list,no_normal_image_copy_path,'R')                    