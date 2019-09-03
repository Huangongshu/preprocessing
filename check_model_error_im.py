# -*- coding: utf-8 -*-
#@author:huan
    
from keras.models import load_model
import numpy as np
from glob import glob
import cv2
from shutil import copy
from functools import partial
from multiprocessing import Pool

def copy_im(move_path,n_class,model,p):
    im=cv2.imread(p)
    im=cv2.resize(im,(224,224))
    b,g,r=cv2.split(im)
    im=cv2.merge((r,g,b))
    im=(im/255.0-0.5)*2
    im=np.expand_dims(im,axis=0) 
    pred=model.predict(im)
    pred=np.where(pred>=0.5,1,0)
    if pred!=n_class:
        copy(p,move_path)

def check_model_error_im(path,move_path,n_class,model_path):  #Used to select pictures of model prediction errors
    p=[x for x in glob(path+'/*.jpg')]
    model=load_model(model_path)
    func=partial(copy_im,move_path,n_class,model)
    pool=Pool(2)
    pool.map(func,p)
    pool.close()
    pool.join()
    
if __name__=='__main__' :
    #model_path='C:/Users/27011/Desktop/mymodel_27.h5'
    model_path='/home/longpeiji/keras_dr/save_model/mymodel_27.h5'
    
    #type1_path='D:/huan/image_assessment/validation/blur'
    #type2_path='D:/huan/image_assessment/validation/no_blur'
    type1_path='/home/longpeiji/image_assessment/validation/blur'
    type2_path='/home/longpeiji/image_assessment/validation/no_blur'
    
    #move_path1='C:/Users/27011/Desktop/blur_error'
    #move_path2='C:/Users/27011/Desktop/no_blur_error'
    move_path1='/home/longpeiji/blur_error'
    move_path2='/home/longpeiji/no_blur_error'
    
    check_model_error_im(type1_path,move_path1,0,model_path)
    check_model_error_im(type2_path,move_path2,1,model_path)
