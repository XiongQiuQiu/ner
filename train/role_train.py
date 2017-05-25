# -*- coding:utf-8 -*-
'''
基于角色标签标注模型训练
input: *.txt
output: start_prob.py
        trans_prob.py
        emit_prob.py
'''
import sys
import os
import re

start_dic = {}
trans_dic = {}
emit_dic = {}
count_dic = {}
pi_dic = {}
states_list = ['A', 'B', 'C', 'D', 'E', 'K', 'L', 'M', 'U', 'V', 'X', 'Y', 'Z']
start_nu = 4
word_nu = 0
start_prob_file = 'start_role_prob.py'
trans_prob_file = 'trans_role_prob.py'
emit_prob_file = 'emit_role_prob.py'

def load_data():
    '''返回句子集合'''
    # _curpath = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__fi le__)))
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('data/')))
    data_file = os.listdir(_data_path)
    if data_file:
        result = set()
        for file in data_file:
            data_file_path = os.path.join(_data_path, file)
            for line in open(data_file_path):
                result.add(line.strip().decode('utf-8'))
        return result

def load_2014():
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014_extract/')))
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


def init():
    global start_nu
    global word_N
    for state in states_list:
        trans_dic[state] = {}
        for state1 in states_list:
            trans_dic[state][state1] = 0.0
    for state in states_list:
        start_dic[state] = 0.0
        emit_dic[state] = {}
        count_dic[state] = 0

def output(lineset):
    '''生成output'''
    start_f = file(start_prob_file, 'w')
    emit_f = file(emit_prob_file, 'w')
    trans_f = file(trans_prob_file, 'w')
    print len(lineset)
    for state_key in start_dic:
        start_dic[state_key] = start_dic[state_key] / len(lineset)
    print >> start_f, start_dic

    for state_key in trans_dic:
        for state_key1 in trans_dic[state_key]:
            trans_dic[state_key][state_key1] = trans_dic[state_key][state_key1] / count_dic[state_key]
    print >>trans_f, trans_dic

    for state_key in emit_dic:
        for word in emit_dic[state_key]:
            emit_dic[state_key][word] = emit_dic[state_key][word] / count_dic[state_key]

    print >>emit_f, emit_dic
    start_f.close()
    emit_f.close()
    trans_f.close()

def calculate(line_set):
    ''''''
    init()
    n = 0
    for line in line_set:
        # if not line:continue
        line_state = get_sign(line)

        for i in range(len(line_state)):
            if i == 0:
                start_dic[line_state[i]] += 1
                count_dic[line_state[i]] += 1
            else:
                trans_dic[line_state[i-1]][line_state[i]] += 1
                count_dic[line_state[i]] += 1
            if not emit_dic[line_state[i]].has_key(line[i]):
                emit_dic[line_state[i]][line[i]] = 0.0
            else:
                emit_dic[line_state[i]][line[i]] += 1
    output(word_set)


if __name__ == '__main__':
    word_set = load_2014()
    # word_set = load_data()
    word_set.union(load_data())
    calculate(word_set)
