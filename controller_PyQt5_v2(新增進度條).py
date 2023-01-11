# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 14:05:58 2022

@author: 06006637
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import os
from yolo import YOLO
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
import threading


"""使用此程式呼叫前端介面UI.py"""

from UI import Ui_MainWindow 


class MainWindow_controller(QtWidgets.QMainWindow):
     
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        
        
    def ButtonClick(self):
        self.qthread = ThreadTask()
        self.qthread.qthread_signal.connect(self.progress_changed) 
        self.qthread.start()
        self.ButtonOn()
        self.qthread.qthread_signal_2.connect(self.ButtonOff) 
        
        
                
    def ButtonOn(self):        
        #執行Detect時禁用按鈕
        self.ui.pushButton_3.setEnabled(False)        
        #啟動按鈕後變換文字
        self.ui.pushButton_3.setText("執行中請稍後")
     
    def ButtonOff(self, value):
        
        if value >= 100:
             #完成Detect 恢復按鈕功能
            self.ui.pushButton_3.setEnabled(True)            
            #完成Detect  後變換文字
            self.ui.pushButton_3.setText("Detect Image")
#        self.ui.pushButton_1.setEnabled(False)
#        self.ui.pushButton_2.setEnabled(False)
#        self.ui.pushButton_4.setEnabled(False)
    
        
    def setup_control(self):
        self.ui.pushButton.clicked.connect(self.open_folder_1)    #設定讀取Img資料夾路徑
        self.ui.pushButton_2.clicked.connect(self.open_folder_2)    #設定存取辨識結果Img資料夾路徑
        self.ui.pushButton_3.clicked.connect(self.ButtonClick)
        self.ui.pushButton_4.clicked.connect(self.clean_folder)    #清除辨識結果資料夾
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)

                   
    def progress_changed(self, value):
        self.ui.progressBar.setValue(value)


    def open_folder_1(self):
        folder_path = QFileDialog.getExistingDirectory(self,
                  "Open folder",
                  "./")                 # start path
        print(folder_path)
        self.ui.show_folder_path_1.setText(folder_path)  
        
        global dir_origin_path
        dir_origin_path = self.ui.show_folder_path_1.toPlainText()
        

    def open_folder_2(self):
        folder_path = QFileDialog.getExistingDirectory(self,
                  "Open folder",
                  "./")                 # start path
        print(folder_path)
        self.ui.show_folder_path_2.setText(folder_path)
 

## 儲存合併圖/一般圖的路徑設定 (二選一)       
        global dir_merge_save_path
        dir_merge_save_path =self.ui.show_folder_path_2.toPlainText()
               
#        global dir_save_path
#        dir_save_path =self.ui.show_folder_path_2.toPlainText()
        
    def clean_folder(self):
        
        import shutil
       
        clean_folder_path = self.ui.show_folder_path_2.toPlainText()
        
        try:
            shutil.rmtree(clean_folder_path)
                
        except OSError as e:
            print(f"Error:{ e.strerror}")


#------------使用QThread避免主介面動作無反應------------------------------------------------------      
class ThreadTask(QThread):
    qthread_signal = pyqtSignal(int)
    qthread_signal_2 = pyqtSignal(int)
    
   
    def start(self):
        threading.Thread(target=self.Model_Detect, daemon=True, args=()).start()  ###將呼叫yolo主程式使用threading進行平行運算 
          
    def Model_Detect(self):
        
        
        if __name__ == "__main__":
            
            yolo = YOLO()
            mode = "dir_predict"
            crop            = False
            count           = False
          
            dir_save_path   =  "img_out1/"

            if mode == "predict":
                while True:
                    img = input('Input image filename:')
                    try:
                        image = Image.open(img)
                    except:
                        print('Open Error! Try again!')
                        continue
                    else:
                        r_image = yolo.detect_image(image, crop = crop, count=count)
                        r_image.show()
            
            elif mode == "dir_predict":

                img_names = os.listdir(dir_origin_path)
                
                classes_nums_sum = [0, 0, 0, 0]    #創建一個list用來統計點數加總，欄位數量需同類別數量
                max_value= 0
                set_value= 0
                global progress_value 
                progress_value = 0
                self.qthread_signal.emit(progress_value)
                self.qthread_signal_2.emit(progress_value)
                #-----------------此段計算總圖檔數，用以繪製進度條------------------------------              
                for path in os.listdir(dir_origin_path):
                    if os.path.isfile(os.path.join(dir_origin_path, path)):
                        max_value += 1 
                print("照片張數計算:",max_value)
               #-----------------------------------------------------------------------------
                from tqdm import tqdm 
                for img_name in tqdm(img_names):
                    
                    set_value += 1 
#                    global progress_value 
                    progress_value = int(set_value*100/max_value)             
                    self.qthread_signal.emit(progress_value)
                    self.qthread_signal_2.emit(progress_value)

                #--------------開始讀取image，執行yolo----------
#                    if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                    if img_name.lower().endswith(('_z.jpg')):   #由於空拍熱影像照片名稱字尾為_T，改以此段過濾非熱影像照片。可見光影像字尾為_Z，可過濾非可見光影像照片
                        image_path  = os.path.join(dir_origin_path ,img_name)
                        image       = Image.open(image_path)
                        r_image , classes_nums , class_names   = yolo.detect_image(image, count = True)  #每張圖片進行yolo.py Detect後，回傳 結果圖、種類點數list 、 種類名稱list
                        
               #------------計算各分類點數加總(用於統計作圖)----------------------------------
                        classes_nums_sum = np.sum([classes_nums_sum ,classes_nums], axis=0).tolist()
                        print("所有圖片累計點數計算" ,classes_nums_sum)
              
               #----------此段為辨識結果圖儲存------------------------------------------------ 
#                        if not os.path.exists(dir_save_path):
#                            os.makedirs(dir_save_path)                       
#                        r_image.save(os.path.join(dir_save_path, img_name.replace(".jpg", ".png")), quality=95, subsampling=0)
                
              #-------------使用此段為同時將原圖+辨識結果合併儲存-------------
                        if not os.path.exists(dir_merge_save_path):
                            os.makedirs(dir_merge_save_path)
              
                        toImage = Image.new('RGB', (1300, 512))
                        image   = Image.open(image_path)
                        toImage.paste(image, (0, 0))
                        toImage.paste( r_image, (650, 0, 650 + image.size[0], 0 + image.size[1])) #函式描述：toImage:背景圖片,paste()函式四個變數分別為：起始橫軸座標，起始縱軸座標，橫軸結束座標，縱軸結束座標；
                        toImage.save( os.path.join(dir_merge_save_path, img_name.replace(".jpg", ".png")), quality=95, subsampling=0)
                    
              #-------------使用此段為各類點數統計作圖-------------
                #print(class_names)
                x = np.arange(len(class_names))
                y = classes_nums_sum
                
                cmap = cm.jet(np.linspace(0, 1, len(class_names)))
                plt.bar(x, y, color=cmap)
                plt.xticks(x, class_names)
                plt.ylabel('Total_Counts')
                plt.title('Detect Result')
                plt.savefig("Detect Result.png")
                plt.close()
                #plt.show()
                
                #-------------------此段做圓餅圖---------------------
                plt.figure(figsize=(6,9))         # 顯示圖框架大小
                separeted = (0, 0.3, 0, 0)   # 依據類別數量，分別設定要突出的
                plt.pie(y,                             # 數值
                       labels = class_names,           # 標籤
                       autopct = "%1.1f%%",            # 將數值百分比並留到小數點一位
                       explode = separeted,             # 設定分隔的區塊位置
                       pctdistance = 0.6,              # 數字距圓心的距離
                       textprops = {"fontsize" : 12},  # 文字大小
                       shadow=True)                    # 設定陰影
                plt.axis('equal')
                plt.title("Pie chart of Detect Result ", {"fontsize" : 18})
                plt.legend(loc = "best")  
                plt.savefig("Pie chart of Detect Result.png",   # 儲存圖檔
                            bbox_inches='tight',               # 去除座標軸占用的空間
                            pad_inches=0.0)                    # 去除所有白邊
                plt.show() 
        
           
                    
if __name__ == '__main__':
    import sys
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec_())