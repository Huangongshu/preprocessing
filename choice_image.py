# -*- coding: utf-8 -*-
#@author:huan

import pandas as pd
import os
import shutil

#all path
         
label_path='D:/huan/视眼膜眼底筛查------20190730/视网膜眼底筛查/眼底筛查AI标签第一批_1.xlsx' 
distinct_image_copy_path='D:/huan/视眼膜眼底筛查------20190730/DR_data/distinct/'
no_distinct_image_copy_path='D:/huan/视眼膜眼底筛查------20190730/DR_data/no_distinct/'
image_base_path='D:/huan/视眼膜眼底筛查------20190730/视网膜眼底筛查/image_data'

#存储对应号码

df = pd.read_excel(label_path)  
left_distinct_list=df[(df.图像不清晰!=1) & (df.眼睛=='左眼')&(df.挂号号码>180000000000)]
right_distinct_list=df[(df.图像不清晰!=1) & (df.眼睛=='右眼')&(df.挂号号码>180000000000)]    
no_left_distinct_list=df[(df.图像不清晰==1) & (df.眼睛=='左眼')&(df.挂号号码>180000000000)] 
no_right_distinct_list=df[(df.图像不清晰==1) & (df.眼睛=='右眼')&(df.挂号号码>180000000000)] 

#复制图片函数

#def choice_i(num_path_list_df,df_index,image_base_path,image_copy_path,split_sy_position,copy_num,eye_type):
def choice_i(num_path_list_df,df_index,image_base_path,image_copy_path,split_sy_position,eye_type):       
    '''
    parameter:
        num_path_list_df: dataframe中挂号号码的列表
        df_index: dataframe中序号的列表
        image_base_path: 存放所有眼睛图片的文件夹地址
        image_copy_path: 复制的图片存放的地址
        copy_num: 复制的挂号号码量
        eye_type: 'L' or 'R'
        
    '''    
#    index=np.random.choice(df_index,copy_num)
#    for i in index:    
    for i in df_index:
        i_path=[os.path.join(image_base_path,str(num_path_list_df[i]),x) for x in os.listdir(image_base_path+'/'+str(num_path_list_df[i]))]
        for d_d in i_path:
            d=d_d.split('_')
            if d[split_sy_position]==eye_type: #d[5]中5表示图片地址分割后，'L'和'R'刚好处于第6段的位置。
                shutil.copy(d_d,image_copy_path) 
            
#提取清晰与不清晰对应眼睛图片
    
choice_i(left_distinct_list.挂号号码,left_distinct_list.index,image_base_path,distinct_image_copy_path,5,'L') 
choice_i(right_distinct_list.挂号号码,right_distinct_list.index,image_base_path,distinct_image_copy_path,5,'R') 
choice_i(no_left_distinct_list.挂号号码,no_left_distinct_list.index,image_base_path,no_distinct_image_copy_path,5,'L') 
choice_i(no_right_distinct_list.挂号号码,no_right_distinct_list.index,image_base_path,no_distinct_image_copy_path,5,'R')            