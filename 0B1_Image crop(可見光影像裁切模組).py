# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 08:37:29 2022

@author: 06006637
"""

import cv2
import os
import numpy as np


"""Step1. 將可見光影像切四等分先切4份"""

dir_origin_path = "C:/Users/06006637/Desktop/yolov4-keras-master/C1-C5"
dir_output_path = "C:/Users/06006637/Desktop/yolov4-keras-master/imgCrop_out"

img_names = os.listdir(dir_origin_path)
from tqdm import tqdm 
for img_name in tqdm(img_names):
    if img_name.lower().endswith(('_z.jpg')):
        image_path  = os.path.join(dir_origin_path ,img_name)
        img = cv2.imread(image_path)
        
    # 裁切區域1 x 與 y 座標（左上角）
        x = 0
        y = 0
        # 裁切區域的長度與寬度
        w = 2592
        h = 1944

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C01_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)
        
        
    # 裁切區域2  x 與 y 座標（右上角）
        x = 2592
        y = 0
        # 裁切區域的長度與寬度
        w = 2592
        h = 1944

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C02_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)
        
    # 裁切區域3  x 與 y 座標（左下角）
        x = 0
        y = 1944
        # 裁切區域的長度與寬度
        w = 2592
        h = 1944

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C03_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)
        
    # 裁切區域4  x 與 y 座標（右下角）
        x = 2592
        y = 1944
        # 裁切區域的長度與寬度
        w = 2592
        h = 1944

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C04_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)
        

"""Step2. 將切完的影像再切四等分"""

dir_origin_path = "C:/Users/06006637/Desktop/yolov4-keras-master/imgCrop_out"
dir_output_path = "C:/Users/06006637/Desktop/yolov4-keras-master/imgCrop_out_final"

img_names = os.listdir(dir_origin_path)
from tqdm import tqdm 
for img_name in tqdm(img_names):
    if img_name.lower().endswith(('_z.jpg')):
        image_path  = os.path.join(dir_origin_path ,img_name)
        img = cv2.imread(image_path)
        
    # 裁切區域1 x 與 y 座標（左上角）
        x = 0
        y = 0
        # 裁切區域的長度與寬度
        w = 1296
        h = 977

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C01_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)
        
        
    # 裁切區域2  x 與 y 座標（右上角）
        x = 1296
        y = 0
        # 裁切區域的長度與寬度
        w = 1296
        h = 977

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C02_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)
        
    # 裁切區域3  x 與 y 座標（左下角）
        x = 0
        y = 977
        # 裁切區域的長度與寬度
        w = 1296
        h = 977

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C03_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)
        
    # 裁切區域4  x 與 y 座標（右下角）
        x = 1296
        y = 977
        # 裁切區域的長度與寬度
        w = 1297
        h = 977

        # 裁切圖片
        crop_img = img[y:y+h, x:x+w]   
        crop_img_name = 'C04_'+ img_name 
        cv2.imwrite(os.path.join(dir_output_path , crop_img_name), crop_img)