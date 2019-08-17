# -*- coding: utf-8 -*-
#@author:huan

from glob import glob
import shutil as sh
import os
def compare_file(move_im_path,goal_path,save_path):
    move_im_path=[os.path.basename(i) for i in glob(move_im_path+'/*.jpg')]
    for i in glob(goal_path+'/*.jpg'):
        if os.path.basename(i) not in move_im_path:
            sh.copy(i,save_path)
            
if __name__=='__main__':
    goal_path1=r'D:\huan\视眼膜眼底筛查------20190730\DR_data\第二批数据\normal2'
    move_im_path1=r'D:\huan\第二批数据过滤\normal2'
    save_path1='D:\huan\第二批数据过滤\delete_no_blur_im'
    
    goal_path2=r'D:\huan\视眼膜眼底筛查------20190730\DR_data\第二批数据\abnormal2'
    move_im_path2=r'D:\huan\第二批数据过滤\abnormal2'
    
    compare_file(move_im_path1,goal_path1,save_path1)
    compare_file(move_im_path2,goal_path2,save_path1)