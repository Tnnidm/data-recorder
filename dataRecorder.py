# used libs
import datetime
import time
import os
import hashlib
import csv

# used modules
import config

class ResultRecoder():
    def __init__(self, name_componant_para):
        
        '''
        读取config中的参数
        '''
        para_dict = dict()
        for paraname, value in config.__dict__.items():
            if type(value) in [int, float, str, bool, list] and not paraname.startswith('_'):
                para_dict.update({paraname: value})

        '''
        初始化日期文件夹位置
        '''
        dt = datetime.datetime.now()
        DATE =  str(dt.month).zfill(2)+str(dt.day).zfill(2)
        MOMENT = str(dt.hour).zfill(2)+str(dt.minute).zfill(2)
        del dt

        '''
        初始化数据文件夹名字
        '''
        RESULT_FILE_NAME = 'exp' + DATE + '_' + MOMENT
        
        for paraname in name_componant_para:
            if paraname in para_dict.keys():
                RESULT_FILE_NAME += '_' + paraname + str(para_dict[paraname])
            else:
                print(paraname + " in name_componant_para is not in config")
                exit()
        
        '''
        为了避免并行时候冲突，采用sha1算法对UNIX时间加上文件夹地址生成一段哈希值，取前6位加在原文件夹名字后面，并生成这个文件夹
        这个文件夹里面有两部分，一个是config文件夹文件，一个是实验结果
        '''
        while True:
            info = str(time.time()) + RESULT_FILE_NAME
            hash_value = hashlib.sha1(info.encode('UTF-8')).hexdigest()[:6]
            RESULT_FILE_NAME_W_HASH = RESULT_FILE_NAME + '_' + hash_value
            RESULT_PATH = os.path.join("result", DATE, RESULT_FILE_NAME_W_HASH)
            if os.path.exists(RESULT_PATH) == False:
                os.makedirs(RESULT_PATH)  
                break

        '''
        存储的CSV路径
        '''
        self.CONFIG_PATH = os.path.join(RESULT_PATH, 'config_' + RESULT_FILE_NAME_W_HASH + '.csv')
        self.DATA_PATH = os.path.join(RESULT_PATH, 'data_' + RESULT_FILE_NAME_W_HASH + '.csv')

        '''
        把config记下来，方便后期复现
        '''
        with open(self.CONFIG_PATH, mode = "w", encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            for paraname, value in para_dict.items():
                csv_writer.writerow([paraname, value])

        '''
        初始化记录空间dict
        整体的结构是{data_name:[data1, data2, ...]}
        '''
        self.result_space = {}

        '''
        csv写入时的顺序
        '''
        self.written_order = []
        
    
    def collect(self, collected_data):
        for key in collected_data.keys():
            if type(collected_data[key]).__name__ == 'ndarray':
                if collected_data[key].ndim == 1:
                    collected_data[key] = collected_data[key].tolist()
                else:
                    print("ERROR: " + key + "in collect is a ndarray with more than 1 dim")
                    exit()
            if key in self.result_space.keys():
                self.result_space[key].append(collected_data[key])
            else:
                self.result_space.update({key: [collected_data[key]]})
            if key not in self.written_order:
                self.written_order.append(key)


    def write(self):
        with open(self.DATA_PATH, mode = "w", encoding='utf-8', newline='') as file:

            '''
            初始化writter
            '''
            csv_writer = csv.writer(file)

            '''
            生成和写入title
            '''
            title_list = []
            for key in self.written_order:
                if type(self.result_space[key][0]).__name__ == 'list':
                    for i in range(len(self.result_space[key][0])):
                        title_list.append(key+"_"+str(i))
                else:
                    title_list.append(key)
            csv_writer.writerow(title_list)

            '''
            写入内容
            '''
            for i in range(len(self.result_space[self.written_order[0]])):
                data_list = []
                for key in self.written_order:
                    if type(self.result_space[key][0]).__name__ == 'list':
                        data_list += self.result_space[key][i]
                    else:
                        data_list.append(self.result_space[key][i])    
                csv_writer.writerow(data_list)