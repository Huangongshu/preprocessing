import os
import pandas as pd
from glob import glob


def judge_illness(string,patt): 
    '''
    Used to determine whether the label exists.
    parameter:
        string: the string you enter that needs to look for the pattern
        patt: the pattern,for exemple:'糖尿病'，'渗出血'
    '''
    t_eye='双眼'
    l_eye='左眼'
    r_eye='右眼'
    
    t_eye_str_order = string.find(t_eye) #Finding the order of pattern in a string
    l_eye_str_order = string.find(l_eye)
    r_eye_str_order = string.find(r_eye) 
    pat_str_order = string.find(patt)
    
    if t_eye_str_order == -1:
        t_eye_str_order = 10000
    
    if l_eye_str_order == -1:
        l_eye_str_order = 20000    
    
    if r_eye_str_order == -1:
        r_eye_str_order = 30000     
    
    rank = [t_eye_str_order, l_eye_str_order, r_eye_str_order, pat_str_order]
    rank = sorted(rank)
    
    if pat_str_order !=-1: #pattern existence
        tem = rank[rank.index(pat_str_order) - 1]    
        if tem == t_eye_str_order:
            return t_eye
        elif tem == l_eye_str_order:
            return l_eye
        else:
            return r_eye
    else:
        
        return -1 #no illness
  

def matching_information(df, seek_columns, positioning_columns, positioning_columns2, pattern, *file_path):
    '''
    seek_columns:the column number of dataframe. We will search for content on the column.  
    positioning_columns :the positioning column number of dataframe,for exemple registered number. 
    positioning_columns2 : eye type
    '''
    file_path_coll = []
    for folder_path in file_path:
        for p in glob(folder_path + '/*.jpg'):
            file_path_coll.append(p)
            
    count = 0
    
    for i in range(len(df)):
        test = judge_illness(df.iloc[i, seek_columns], pattern) 
        seek_num = df.iloc[i, positioning_columns]
        if test == '双眼':
            if df.iloc[i, positioning_columns] == '左眼':
                eye_type = 'L'
            else: 
                eye_type = 'R'
                
            for path in file_path_coll:
                if str(seek_num) in path and eye_type in path:
                    count += 1
        if (test == '左眼') and (df.iloc[i, positioning_columns2] == '左眼'):
            for path in file_path_coll:
                if str(seek_num) in path and 'L' in path:
                    count += 1        
        if (test == '右眼') and (df.iloc[i, positioning_columns2] == '右眼'):
            for path in file_path_coll:
                if str(seek_num) in path and 'R' in path:
                    count += 1  
    return count


if __name__ == '__main__':
    #dataframe path
    df_path = '/home/huan/huan/眼底筛查AI总标签.xlsx'
    
    #image path
    first_two_blur = '/home/huan/huan/firt_twodata/blur'
    first_two_no_blur = '/home/huan/huan/firt_twodata/clear'
    third_data_abnormal = '/home/huan/huan/third_data/abnormal'
    third_data_normal = '/home/huan/huan/third_data/normal'
    third_data_blur = '/home/huan/huan/third_data/blur'
    
    seek_columns = 9
    positioning_columns = 0
    positioning_columns2=2
    
    pattern = '眼底影像模糊'
    
    df=pd.read_excel(df_path, index_col = 0)
    count=matching_information(df, seek_columns, positioning_columns, positioning_columns2, pattern, first_two_blur,\
                               first_two_no_blur, third_data_abnormal, third_data_normal, third_data_blur)
    print(count)
