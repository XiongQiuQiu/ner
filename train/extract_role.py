# -*- coding=utf-8 -*-
import os

def load_word_data():
    '''返回句子集合'''
    # _curpath = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__fi le__)))
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('word/')))
    data_file = os.listdir(_data_path)
    if data_file:
        result = set()
        for file in data_file:
            data_file_path = os.path.join(_data_path, file)
            for line in open(data_file_path):
                result.add(line.strip().decode('utf-8'))
        return result

def word_role(word):
    word_set = load_word_data()
    l = len(word)
    if l == 2 and word in word_set:
        word_state = ['Y']
    elif l == 2:
        word_state = ['B', 'E']
    elif l == 3 and word[0:2] in word_set:
        word_state = ['X', 'D']
    elif l == 3:
        word_state = ['B', 'C', 'D']


def ex_role(line):
    line_list = line.split()
    final = []
    two_gram = []
    for i in range(len(line_list)-1):
        two_gram.append((line_list[i], line_list[i+1]))
    for i, word_two_gram in enumerate(two_gram):
        one_word_list = word_two_gram[0].split('/')
        two_word_list = word_two_gram[1].split('/')
        if one_word_list[1] != 'nr' and two_word_list[1] == 'nr':
            one_word_list[1] = 'K'
            two_word_list[1] = word_role(two_word_list[0])
        elif one_word_list[1] == 'nr' and two_word_list[1] != 'nr':
            one_word_list[1] = word_role(one_word_list[0])
            two_word_list[1] = 'L'
        else:
            one_word_list[1] = 'A'
            two_word_list[1] = 'A'
            if final[-1][0] == one_word_list[0]:
            final.append(one_word_list)

        final.append()




def extract_2014():
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014/')))
    write_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014_extract/')))
    dir_file = os.listdir(_data_path)
    result = set()
    for dir in dir_file:
        dir_file_path = os.path.normpath(os.path.join(_data_path, os.path.dirname(dir+'/')))
        file_name_list = os.listdir(dir_file_path)
        for file in file_name_list:
            file_path = os.path.join(dir_file_path, file)
            with open(file_path) as f:
                for line in f:
                    result.add(line.strip().decode('utf-8'))
    return result