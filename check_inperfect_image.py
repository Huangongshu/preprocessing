# -*- coding: utf-8 -*-
#@author:huan

import os
import skimage.io as io
class CheckImage(object):

    def __init__(self,im_path):
        self.im_path=im_path
#        print(self.im_path)
        with open(self.im_path, "rb") as f:
            f.seek(-4, 2)
            self.im_text = f.read()
            f.close()

    def check_jpg_jpeg(self):
        """检测jpg图片完整性，完整返回True，不完整返回False"""
        buf = self.im_text
        return buf.endswith(b'\xff\xd9')

    def check_png(self):
        """检测png图片完整性，完整返回True，不完整返回False"""
        buf = self.img_text
        return buf.endswith(b'\xaeB`\x82')
    
    def check_im_size(self):
        im=io.imread(self.im_path)
#        print(im.shape[1])
        if im.shape[1] >=1800 and im.shape[0]>=1800: #排除不高清图片
            return True
        
if __name__=='__main__':
    abnormal_base_path='D:/huan/视眼膜眼底筛查------20190730/DR_data/no_distinct'
    normal_base_path='D:/huan/视眼膜眼底筛查------20190730/DR_data/distinct'
  
    
    def check_data(base_path):
        d=[base_path+'/'+x for x in os.listdir(base_path)]
        for im_path in d:
            try:
                c=CheckImage(im_path)
                d=c.check_jpg_jpeg()
                if d!=True:
                    os.remove(im_path)
                    d1=c.check_im_size()
                    if d1!=True:
                        os.remove(im_path) #删除不完整图片
            except OSError:
                print('出现异常文件,路径为：',im_path)
                os.remove(im_path)
                
                
    check_data(abnormal_base_path)
    check_data(normal_base_path)
