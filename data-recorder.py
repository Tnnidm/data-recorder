from datetime import datetime
import os, shutil
import random
import string

# todo:
# 1. 通过args记录实验参数
# 2. 仿造wandb使用dict保存数据，而后使用csv保存

class DataRecorder():
    def __init__(self, result_folder_location):
        dt = datetime.now() #创建一个datetime类对象
        DATE = str(dt.month).zfill(2)+str(dt.day).zfill(2)
        TIME = str(dt.hour).zfill(2)+str(dt.minute).zfill(2)
        del dt

        DATE_folder_dir = result_folder_location + DATE + '/'
        if os.path.exists(DATE_folder_dir) == False:
            os.makedirs(DATE_folder_dir);
        
        self.DATE_TIME_folder_dir = DATE_folder_dir + TIME + '_' + \
            ''.join(random.sample(string.ascii_letters + string.digits, 16)) + '/'
        while True:
            if os.path.exists(self.DATE_TIME_folder_dir) == False:
                os.makedirs(self.DATE_TIME_folder_dir)
            else:
                self.DATE_TIME_folder_dir = DATE_folder_dir + TIME + '_' + \
                    ''.join(random.sample(string.ascii_letters + string.digits, 16)) + '/'
        
