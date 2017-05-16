#-*-coding:utf-8
import os
import sys

def load_2014():
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014/')))
    dir_file = os.listdir(_data_path)
    result = set()
    for dir in dir_file:
        dir_file_path = os.path.normpath(os.path.join(_data_path, os.path.dirname(dir+'/')))
        file_name_list = os.listdir(dir_file_path)
        for file in file_name_list:
            file_path = os.path.join(dir_file_path, file)
            print dir_file_path, file_path
            with open(file_path) as f:
                for line in f:
                    result.add(line.strip().decode('utf-8'))
    return result