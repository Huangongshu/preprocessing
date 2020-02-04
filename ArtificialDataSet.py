# -*- coding: utf-8 -*-
#author:huan

import json
import numpy as np
import cv2
import os
import time
os.chdir('D:/python/model/')
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

class ArtificialDataSet():
    #use to get the artificial chromosome data
    def __init__(self, datafile, save_path = None):
        self.data_path = datafile
        self.save_path = save_path
        try:
            self._dataset = list(json.load(open(self.data_path, 'r')).values())
            self.data_length = len(self._dataset)
            self.dataset = iter(self._dataset)
            print('complete the init')
        except:
            raise 'json file read failed'
 
           
    @property        
    def _single_information(self):
        #get the single picture information
        print('read a data')
        return next(self.dataset)
 
    
    @property
    def get_next_info(self):
        #use to get an information of the chromosome image
        self._im_data = self._single_information
        self._file_path = self._im_data['filename']
        self._im = cv2.imread('./chromosome/' + self._file_path)
        
        self.original_h, self.original_w, self._c = self._im.shape
        self._chromosome_num = len(self._im_data['regions'])  
        
        #use to save the new data        
        self._box_information_collection = []
        self._rotate_box_collection = []
        self._rotate_box_contour_collection = []
        self._rotate_angle_collection = []
 
        self.flag = self._chromosome_num      
        self._update_base_point()
        self._get_rotate_empty_template()
        
    def get_new_im(self):
        #get the new artificial image        
        for i in range(self.data_length): 
            self.image_number = i
            self.get_next_info
            self.create_singe_im()


    def create_singe_im(self):
        start = time.time()
        while self.flag:
            fail_flag = 0
            overlap = 1     
            self._classes = int(self.flag % self.chromosome_num)
            self._get_box(self.flag % self.chromosome_num)     
            self.base_point_index = [x for x in range(len(self.base_point))]            
            while overlap:
                self._coordinate_distributor()                
                for _ in range(10):       
                    self._rotate()                    
                    overlap = self._judge_out_of_boundary()
                    if overlap:
                        continue                    
                    overlap += self._judge_Intersection()
                    if overlap == 0:
                        break
                    
                fail_flag += 1
                if fail_flag > 2000 and overlap:
                    fail_flag = 10000
                    self._update_all_rotate_data()
                    print('get the image again')
                    break
            if fail_flag < 3000:   
                self.flag -= 1                
                self._im_rotate()
                self._contour_rotate()            
                self.base_point.pop(self.del_cord_index)
                # print('complete single:', int(self.flag % self.chromosome_num))
                self.concat_image()            
                #use to judge the intersection
                self._rotate_box_collection.append(((self._center_x + self._new_pos_x,
                                                    self._center_y + self._new_pos_y),
                                                    (self._w, self._h), self._angle * 180 / np.pi))
                
                self._box_information_collection.append(((int(self._x0 + self._new_pos_x + self._w * 0.5),
                                                         int(self._y0 + self._new_pos_y + self._h * 0.5)),
                                                        (self._w, self._h),
                                                        self._angle * 180 / np.pi))
        end = time.time()
        print('create singe image use time:\n', end - start)    
        cv2.imwrite(self.save_path + '/concat_im' + str(self.image_number) + '.png',
                    self.concat_im.astype(np.uint8))

        # cv2.imwrite(self.save_path + '/concat_mask' + str(self.image_number) + '.png',
        #             self.concat_mask.astype(np.uint8))
 
    def _rotate(self):
        '''
        use to rotate the single chromosome image, and update 
        the information of coordinate and contour of the chromosome
        '''
        self._update_angle()        
        self._b_matrix()
        self._f_matrix()
        self._box_rotate()

    def _get_box(self, num_box):
        #get the single chromosome box regions
        self._num_box = str(num_box)
        self._w = self._im_data['regions'][self._num_box]['width']
        self._h = self._im_data['regions'][self._num_box]['height']
        self._x0 = self._im_data['regions'][self._num_box]['x']
        self._y0 = self._im_data['regions'][self._num_box]['y']   
        
        self._contour_x = self._im_data['regions'][self._num_box]['shape_attributes']['x']
        self._contour_y = self._im_data['regions'][self._num_box]['shape_attributes']['y']        
        self._contour = [[int(x - self._x0), int(y - self._y0)] 
                        for x, y in zip(self._contour_x, self._contour_y)]

        # use to clear the noisy of the image of the box, as centromere line        
        self._temp = cv2.fillPoly(np.zeros_like(self._im), [np.asarray([(int(x),
                int(y)) for x, y in zip(self._contour_x, self._contour_y)])],(1, 1, 1))
        self._temp_pad = np.copy(self._temp)
        self._temp_pad[self._temp_pad[:, :, :] == 0] = 255           
        self._temp_pad[self._temp_pad[:, :, :] == 1] = 0
     
        self._temp_im = np.multiply(self._im, self._temp)
        self._temp_im += self._temp_pad
        self._im_box = self._temp_im[self._y0: self._y0 + self._h, 
                                self._x0: self._x0 + self._w].astype(int)             


    def concat_image(self):
        #use to concat the single chromosome

        for y in range(self._newh):
            for x in range(self._neww):
                pos_y = y + self._new_pos_y
                pos_x = x + self._new_pos_x

                if all(self._rotate_im[y, x, :] <= 250): 
                    self.concat_im[pos_y][pos_x] = self._rotate_im[y][x]
                    self.concat_mask[pos_y][pos_x] = self._classes + 1


    def _judge_out_of_boundary(self):
        try:
            #use to judge the image whether out of boundary
            if self._newh + self._new_pos_y >= self.original_h\
                or self._neww + self._new_pos_x >= self.original_w\
                or self._new_pos_x < 0 or self._new_pos_y < 0:
                    raise OverflowError                    
            return 0
        except:
            # print('out of boundary')
            return 1                     
        
    def _update_base_point(self, interval = 10):
        x = range(0, int(0.9 * self.original_w), interval)
        y = range(0, int(0.9 * self.original_h), interval)
        x, y = np.meshgrid(x, y)
        x = x.reshape(-1)
        y = y.reshape(-1)
        self.base_point = [(i, j) for i, j in zip(x, y)]  
        
    def _update_all_rotate_data(self):
        #when the number of failures reaches a certain number, start over
        self.flag = self._chromosome_num
        self._get_rotate_empty_template()
        self._update_base_point()     
        self._rotate_box_collection = []
        self._box_information_collection = []
     
    def _update_angle(self):
        self._angle = round(np.random.randint(0, 359, 3)[0] * np.pi / 180, 4)     
        self._neww = int(self._w * abs(np.cos(self._angle)) + 
                        self._h * abs(np.sin(self._angle))) + 1    
        self._newh = int(self._w * abs(np.sin(self._angle)) + 
                        self._h * abs(np.cos(self._angle))) + 1        

    def _coordinate_distributor(self):
        #use to generator the angel and position of the new image        
        self._update_offset()   #update offset value            
        self._update_new_pos()   #update box top left point value     

    def _update_offset(self):
        #get the single box offset value
        self.offset_x = np.random.randint(-0.01 * self.original_w,
                                          0.01 * self.original_w, 1)[0]
        self.offset_y = np.random.randint(-0.01 * self.original_h,
                                          0.01 * self.original_h, 1)[0]  

    def _update_new_pos(self):
        # base_point = self.base_point.pop(np.random.randint(0,
        #                                 len(self.base_point), 1)[0]) 
        if len(self.base_point_index) == 0:
            self.base_point_index = [x for x in range(len(self.base_point))]
        temp = np.random.randint(0, len(self.base_point_index), 1)[0]
        self.del_cord_index = self.base_point_index.pop(temp)         
        base_point = self.base_point[self.del_cord_index]      
        self._new_pos_x = base_point[0] + self.offset_x
        self._new_pos_y = base_point[1] + self.offset_y  
        
    def _b_matrix(self):
        #backward matrix use to fill the pixel in the new image
        self._back_m = np.array([[1, 0, 0], [0, -1, 0], [-0.5 * self._neww,
                                 0.5 * self._newh, 1]])
        self._back_m = self._back_m.dot(np.array([[np.cos(self._angle), 
                        np.sin(self._angle), 0], [-np.sin(self._angle), 
                        np.cos(self._angle), 0], [0, 0, 1]]))
        self._back_m = self._back_m.dot(np.array([[1, 0, 0], [0, -1, 0], 
                                            [0.5 * self._w, 0.5 * self._h, 1]]))   
             
    def _im_rotate(self):    
        #use to rotate the box of the single chromosome
        self._rotate_im =  np.ones((self._newh, self._neww, self._c), 
                                   dtype = float) * 255.0
        
        for x in range(self._neww):
            for y in range(self._newh):
                srcpos = np.array([x, y, 1]).dot(self._back_m)
                if srcpos[0] >= 0 and srcpos[0] < self._w and srcpos[1] >= 0 \
                        and srcpos[1] < self._h:
                    x0, y0 = int(srcpos[0]), int(srcpos[1])
                    if x0 < self._w - 1 and y0 < self._h -1:
                        val_y0 = self._im_box[y0][x0] + (self._im_box[y0][x0 + 1] - 
                                       self._im_box[y0][x0]) * (srcpos[0] - x0)
                        val_y1 = self._im_box[y0 + 1][x0] + (self._im_box[y0 + 1][x0 + 1] - 
                                       self._im_box[y0 + 1][x0]) * (srcpos[0] - x0)
                        self._rotate_im[y][x] = val_y0 + (val_y1 - val_y0) * (srcpos[1] - y0)

    def _f_matrix(self):  
        #forward matrix use to transform the contour in the new image        
        self._forw_m = np.array([[1, 0, 0], [0, -1, 0], 
                                [-0.5 * self._w, 0.5 * self._h, 1]])
        self._forw_m = self._forw_m.dot(np.array([[np.cos(self._angle), 
                           -np.sin(self._angle), 0], [np.sin(self._angle), 
                           np.cos(self._angle), 0], [0, 0, 1]]))
        self._forw_m = self._forw_m.dot(np.array([[1, 0, 0], [0, -1, 0], 
                            [0.5 * self._neww, 0.5 * self._newh, 1]])) 

    def _contour_rotate(self):
        #get the contour after the chromosomme rotation
        new_contour = []
        for c in self._contour:
            new_c = np.asarray([c[0], c[1], 1]).dot(self._forw_m)
            new_contour.append([int(new_c[0]), int(new_c[1])])
        self._contour = new_contour
 
       
    def _box_rotate(self):
        #get the box regions after the chromosomme rotation   
        #the point in the top left corner, riginal point is (0, 0)
        rotated_box_x0, rotated_box_y0, _ = np.asarray([0, 0, 1]).dot(self._forw_m) 
        
        #the point in the top right corner
        rotated_box_x00, rotated_box_y00, _ = np.asarray([self._w, 0, 1]).dot(self._forw_m) 
        
        #the point in the down left corner
        rotated_box_x11, rotated_box_y11, _ = np.asarray([0, self._h, 1]).dot(self._forw_m)

        #the point in the down right corner
        rotated_box_x1, rotated_box_y1, _ = np.asarray([self._w, self._h, 1]).dot(self._forw_m)       
        self._x_min = min(rotated_box_x0, rotated_box_x00, rotated_box_x11, rotated_box_x1)
        self._x_max = max(rotated_box_x0, rotated_box_x00, rotated_box_x11, rotated_box_x1)        
        self._y_min = min(rotated_box_y0, rotated_box_y00, rotated_box_y11, rotated_box_y1)
        self._y_max = max(rotated_box_y0, rotated_box_y00, rotated_box_y11, rotated_box_y1)              

        #Calculate the midpoint of the box to prepare the box for correction. use the 
        self._center_x, self._center_y, _ = np.asarray([self._w * 0.5,\
                                            self._h * 0.5, 1]).dot(self._forw_m)   

    def _get_rotate_empty_template(self):
        self.concat_im = np.ones_like(self._im).astype(float) * 255.0
        self.concat_mask = np.zeros_like(self._im).astype(float)
  
    
    def _judge_Intersection(self):
        b = ((self._center_x + self._new_pos_x, self._center_y + self._new_pos_y),
                          (self._w, self._h), self._angle * 180 / np.pi)
        for i in range(len(self._rotate_box_collection)):
            
            res = cv2.rotatedRectangleIntersection(self._rotate_box_collection[i], b)
            
            if  res[0] != 0:
                # print('overlap')
                return 1
        return 0
        
    def generator_overlap_mask(): #都给不同染色的掩膜，并对掩膜进行合并。再分别提取轮廓。
        #use to generator the new mask when the chromosome is overlap, use cv2.findContour()   
        pass


    def add_random_bg(self):
        #use to add the random background
        pass


    @property
    def im_shape(self):
        return self._im.shape

    @property
    def chromosome_num(self):
        return self._chromosome_num
    
    @property    
    def get_orignal_coordinate(self):
        return self._box_information_collection

    @property    
    def get_rotate_coordinate(self):
        return self._rotate_box_collection

    @property    
    def angle(self):
        return self._angle * 180 / np.pi
    
    @property
    def show_single_box(self):
        cv2.imshow('box', self._im_box.astype(np.uint8))   
        
    @property
    def show_single_box_contour(self):
        self._im_contour = cv2.polylines(np.copy(self._im_box), 
                        [np.array(self._contour)], 1, color = (0, 0, 255))       
        cv2.imshow('contour',self._im_contour.astype(np.uint8))
              
    @property        
    def show_single_rotate_box(self):
        cv2.imshow('rotate_im', self._rotate_im.astype(np.uint8))
        
    @property        
    def show_single_rotate_contour(self):
        self._rotate_contour = cv2.polylines(np.copy(self._rotate_im), 
                        [np.array(self._contour)], 1, color = (0, 0, 255))       
        cv2.imshow('rotate_contour',self._rotate_contour.astype(np.uint8))        

    @property        
    def show_single_rotate_mask(self):
        self._rotate_mask = cv2.fillPoly(np.copy(self._rotate_im), 
                        [np.array(self._contour)], color = (0, 210, 200))       
        cv2.imshow('rotate_mask',self._rotate_contour.astype(np.uint8))  
       
data = ArtificialDataSet('./chromosome/via_region_data.json', 
                          save_path = 'C:/Users/huan/Desktop/artificial')
data.get_new_im()        
# In[0]      
# data = ArtificialDataSet('./chromosome/via_region_data.json', 
#                          save_path = 'C:/Users/huan/Desktop/artificial')

# data.get_next_info
# data.image_number = 1
# data.create_singe_im()
# b = data.get_rotate_coordinate
# c = []
# for i in range(len(b)):
#     for j in range(i + 1, len(b)):
#         res = cv2.rotatedRectangleIntersection(b[i], b[j])
#         if  res[0] != 0:
#             c.append(res)
#             print(i,'    ',j)
# In[1]
# import cv2
# import numpy as np
# import os
# from glob import glob        

# def transform(gray, h, w, classes_num):
#     temp = np.zeros((h, w, classes_num))
#     for i in range(h):
#         for j in range(w):
#             value = gray[i, j]
#             if value != 0:
#                 temp[i][j][value] = 1
#                 # print(1)
#     return temp

# def draw(path, save_path, num):
#     im = cv2.imread(path)  
#     h, w, c = im.shape       
#     gray = transform(im[:, :, 0], h, w, 47) 
#     for i in range(47):       
#         omp = gray[:, :, i].astype(np.uint8) * 50
#         b, _ = cv2.findContours(omp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         cv2.drawContours(omp, b, 0, 200, 1)
#         cv2.imwrite(save_path + '/' + str(num) + str(i) + '.png', omp)
 
# save_path = 'C:/Users/huan/Desktop/test2'   
# if os.path.exists(save_path) == False:
#     os.makedirs(save_path)
# # im = cv2.imread('C:/Users/huan/Desktop/test/concat_mask31.png')    
# path = [x for x in glob('C:/Users/huan/Desktop/artificial/concat_mask*')]
# for i, p in enumerate(path):
#     draw(p, save_path, i)
