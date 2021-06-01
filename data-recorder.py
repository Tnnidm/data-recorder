from datetime import datetime
import os, shutil
import random
import string
import csv

# todo:
# 1. 通过args记录实验参数
# 2. 仿造wandb使用dict保存数据，而后使用csv保存 (done)
    # 2.1 动态更新第一行的数据title

class DataRecorder():
    def __init__(self, result_folder_location, csv_recoder = False):
        dt = datetime.now() #创建一个datetime类对象
        DATE = str(dt.month).zfill(2)+str(dt.day).zfill(2)
        TIME = str(dt.hour).zfill(2)+str(dt.minute).zfill(2)
        del dt

        DATE_folder_dir = result_folder_location + DATE + '/'
        if os.path.exists(DATE_folder_dir) == False:
            os.makedirs(DATE_folder_dir);
        
        self.DATE_TIME_folder_dir = DATE_folder_dir + TIME + '_' + \
            ''.join(random.sample(string.ascii_letters + string.digits, 6)) + '/'
        while True:
            if os.path.exists(self.DATE_TIME_folder_dir) == False:
                os.makedirs(self.DATE_TIME_folder_dir)
            else:
                self.DATE_TIME_folder_dir = DATE_folder_dir + TIME + '_' + \
                    ''.join(random.sample(string.ascii_letters + string.digits, 6)) + '/'
    
        if csv_recoder == True:
            self.data_csv = 'data-'+self.DATE_TIME_folder_dir[-11:-1]
            self.data_title_list = []
    
    def folder_location(self):
        return self.DATE_TIME_folder_dir
    
    def log(self, inform):
        for key in inform.keys():
            if key not in self.data_title_list:
                self.data_title_list.append(key)
        inform_line = []
        for i in range(len(self.data_title_list)):
            if self.data_title_list[i] in inform.keys():
                inform_line.append(str(inform[self.data_title_list[i]]))
            else:
                inform_line.append(' ')
        with open(self.data_csv, mode = "a+", encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(inform_line)
            file.flush()

