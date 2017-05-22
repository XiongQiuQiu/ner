# -*- coding=utf-8 -*-
import os


def load_word_data():
    '''返回人名集合'''
    # _curpath = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('data/')))
    data_file = os.listdir(_data_path)
    if data_file:
        result = set()
        for file in data_file:
            data_file_path = os.path.join(_data_path, file)
            for line in open(data_file_path):
                result.add(line.strip().decode('utf-8'))
        return result


def name_word_role(word, word_set):
    l = len(word)
    if l == 2 and word in word_set:
        word_state = (word, 'Y')
    elif l == 2:
        word_state = [[word[0], 'B'], [word[1], 'E']]
    elif l == 3 and word[0:2] in word_set:
        word_state = [[word[0:2], 'X'], [word[2], 'D']]
    elif l == 3:
        word_state = [[word[0], 'B'], [word[1], 'C'], [word[2], 'D']]
    try:
        return word_state
    except:
        print word

def ex_role(line):
    word_set = load_word_data()
    line_list = line.split()
    final = []
    two_gram = []
    for i in range(len(line_list)-1):
        two_gram.append((line_list[i], line_list[i+1]))
    for i, word_two_gram in enumerate(two_gram):
        one_word_list = word_two_gram[0].split('/')
        two_word_list = word_two_gram[1].split('/')
        if one_word_list[1] != 'nr' and two_word_list[1] == 'nr':
            if final[-1][0] == one_word_list[0] and final[-1][1] == 'L':
                final[-1][1] = 'M'
                two_word_list = name_word_role(two_word_list[0], word_set)
                final.extend(two_word_list)
                continue
            one_word_list[1] = 'K'
            two_word_list = name_word_role(two_word_list[0], word_set)
            final.append(one_word_list)
            final.extend(two_word_list)
        elif one_word_list[1] == 'nr' and two_word_list[1] != 'nr':
            two_word_list[1] = 'L'
            final.append(two_word_list)
        else:
            one_word_list[1] = 'A'
            final.append(one_word_list)
    return final


def extract_2014():
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014/')))
    _write_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014_extract/')))
    dir_file = os.listdir(_data_path)
    for dir in dir_file:
        write_file_path = os.path.normpath(os.path.join(_write_path, os.path.dirname(dir+'/')))
        dir_file_path = os.path.normpath(os.path.join(_data_path, os.path.dirname(dir+'/')))
        file_name_list = os.listdir(dir_file_path)
        for file in file_name_list:
            file_path = os.path.join(dir_file_path, file)
            write_path = os.path.join(_write_path, file)
            with open(file_path) as f:
                for line in f:
                    w_write_list = ex_role(line.strip().decode('utf-8'))
                    write_line = ' '.join(i[0] + '/' + i[1] for i in w_write_list)
                    f = open(write_path, 'w')
                    f.write(write_line.encode('utf8'))
                    f.close()

if __name__ == '__main__':
    extract_2014()