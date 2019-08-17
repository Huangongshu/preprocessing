# -*- coding: utf-8 -*-
#@author:huan

import cv2
import numpy as np
from glob import glob
import os
from multiprocessing import Pool
from functools import partial

def transparent_im(save_im_path,path):
    img = cv2.imread(path)
    b_channel, g_channel, r_channel = cv2.split(img)
    img=np.copy(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    alpha_channel[(img[:,:,0]==0)&(img[:,:,1]==0)&(img[:,:,2]==0)] = 0 #为0部分就显示透明
    alpha_channel[(img[:,:,0]<=10)&(img[:,:,1]<=10)&(img[:,:,2]<=10)] = 0
    img_BGRA = cv2.merge((b_channel,g_channel,r_channel,alpha_channel))
#    img_t=cv2.merge((r_channel,g_channel,b_channel,alpha_channel))
    cv2.imwrite(save_im_path+'/'+str(os.path.splitext(os.path.basename(path))[0])+".png", img_BGRA)


def preprocessing_im(im_base_path,save_im_path):
    for p in glob(im_base_path+'/*.jpg'):
        transparent_im(p,save_im_path)
        
if __name__=='__main__':  
#    im_path1='D:/huan/the_second_filtered_image/blur2'
#    im_save='D:/huan/transparent_im'
#    im_path2='D:/huan/the_second_filtered_image/normal2'
    
    im_path1='/home/longpeiji/the_second_filtered_image/blur2'    
    im_save='/home/longpeiji/transparent_im'
    path1=[x for x in glob(im_path1+'/*.jpg')]  
    num1=[os.path.splitext(os.path.basename(x))[0] for x in im_path1]
    
    pool=Pool(10)  
    func1=partial(transparent_im,im_save)  #利用多进程进行任务处理
    pool.map(func1,path1)
    pool.close()
    pool.join()
    
#    preprocessing_im(im_path,im_save)
#    transparent_im('D:/learning/190702519837_20190702_110322_Color_R_013.jpg','D:/')
