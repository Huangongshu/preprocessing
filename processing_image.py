# -*- coding: utf-8 -*-
#@author:huan

import matplotlib.pyplot as plt
import cv2
from os.path import join,basename
 
def opencv_clahe(im_path,GridSize,clipLimit,processing_im_save_path,comprated_im_save_path):
    plt.figure(figsize=(20,10),dpi=300) #横着放的对比图，应该宽大于高才好看
    img = cv2.imread(im_path,cv2.IMREAD_COLOR) #中文路径会出错
    b,g,r = cv2.split(img)
    img1=cv2.merge([r,g,b])
    s1=plt.subplot(1,2,1)
    s1.set_title('%s'%'original')
    plt.imshow(img1)
    
#    img=cv2.fastNlMeansDenoisingColored(img,None, 5, 5)  #Non local means denoising 
#    b,g,r = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=GridSize)  #clipLimit对比度的阈值，titleGridSize进行像素均衡化的网格大小 
    b = clahe.apply(b)
    g = clahe.apply(g)
    r = clahe.apply(r)       
    img = cv2.fastNlMeansDenoisingColored(cv2.merge([b,g,r]),None, 5, 5) #去噪
    b,g,r=cv2.split(img)    
    cv2.imwrite(join(processing_im_save_path,basename(im_path)),img,[cv2.IMWRITE_JPEG_QUALITY,100])
    
    img2=cv2.merge([r,g,b])
    s2=plt.subplot(1,2,2)
    s2.set_title('%s'%'processing')
    plt.xticks([])  #去掉x轴
    plt.yticks([])  #去掉y轴
    plt.axis('off')  #去掉坐标轴
    plt.imshow(img2)
  
    plt.savefig(join(comprated_im_save_path,basename(im_path))) #保存对比图
    plt.close()#每次都得关闭当前窗口不然会一直保存在哪里，占用大量内存。
    