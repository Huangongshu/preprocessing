# -*- coding: utf-8 -*-
#@author:huan

from processing_image import opencv_clahe
from glob import glob
import os

def preprocessing_im(im_path,processing_path,comprated_path,clipLimit=1.5,gridsize=20):
    
    try:
        c=len(clipLimit) #为列表形式时
    
    except TypeError: #
        c=1     #不是列表时
        
    try:
        g=len(gridsize)
    
    except TypeError:
        g=1  
        
    if c>1 and g==1:
        for num,value in enumerate(clipLimit):
            os.makedirs(processing_path+'/'+str(value))
            os.makedirs(comprated_path+'/'+str(value))
            proc_path=processing_path+'/'+str(value)
            comp_path=comprated_path+'/'+str(value)    
            for i_path in glob(im_path+'/*.jpg'):
                opencv_clahe(i_path,(gridsize,gridsize),value,proc_path,comp_path)  
    
    elif  g>1 and c==1: 
        for num,value in enumerate(gridsize):
            os.makedirs(processing_path+'/'+str(value))
            os.makedirs(comprated_path+'/'+str(value))
            proc_path=processing_path+'/'+str(value)
            comp_path=comprated_path+'/'+str(value)    
            for i_path in glob(im_path+'/*.jpg'):
                opencv_clahe(i_path,(value,value),clipLimit,proc_path,comp_path) 
    else:
            os.makedirs(processing_path+'/'+str(clipLimit)+'and'+str(gridsize))
            os.makedirs(comprated_path+'/'+str(clipLimit)+'and'+str(gridsize))
            proc_path=processing_path+'/'+str(clipLimit)+'and'+str(gridsize)
            comp_path=comprated_path+'/'+str(clipLimit)+'and'+str(gridsize)   
            for i_path in glob(im_path+'/*.jpg'):
                opencv_clahe(i_path,(gridsize,gridsize),clipLimit,proc_path,comp_path)  

if __name__=='__main__':
    
    #im_base_path='/home/longpeiji/the_second_filtered_image/abnormal2'
    #processing_path1='/home/longpeiji/processing_image/Variable_clipLimit'
    #comprated_path1='/home/longpeiji/compare_image/Variable_clipLimit'
    #processing_path2='/home/longpeiji/processing_image/Variable_gridsize'
    #comprated_path2='/home/longpeiji/compare_image/Variable_gridsize'
    
    #im_base_path='D:/huan/the_second_filtered_image/abnormal2'
    #processing_path1='D:/huan/processing_image/Variable_clipLimit'
    #comprated_path1='D:/huan/compare_image/Variable_clipLimit'
    #processing_path2='D:/huan/processing_image/Variable_gridsize'
    #comprated_path2='D:/huan/compare_image/Variable_gridsize'
    
    im_base_path='D:/huan/test'
    processing_path='C:/Users/27011/Desktop/processing_image'
    comprated_path='C:/Users/27011/Desktop/compare_image'
    
    clipLimit=[0.5,0.8]
    gridsize=[20,23,25,28,30,35]
    #preprocessing_im(im_base_path,processing_path1,comprated_path1,clipLimit,20)           
    #preprocessing_im(im_base_path,processing_path2,comprated_path2,1,gridsize) 
    preprocessing_im(im_base_path,processing_path,comprated_path,1,20) 
