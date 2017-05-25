# -*- coding=utf-8 -*-
import os
import log

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
        word_state = [[word, 'Y']]
    elif l == 2:
        word_state = [[word[0], 'B'], [word[1], 'E']]
    elif l == 3 and word[0:2] in word_set:
        word_state = [[word[0:2], 'X'], [word[2], 'D']]
    elif l == 3:
        word_state = [[word[0], 'B'], [word[1], 'C'], [word[2], 'D']]

    return word_state



def init(word, word_set):
    word = word.split('/')
    if word[1] != 'nr':
        word[1] = 'A'
        return [word]
    else:
        word = name_word_role(word[0], word_set)
    return word


def ex_role(line):
    word_set = load_word_data()
    line_list = line.split()
    two_gram = []
    for i in range(len(line_list)-1):
        two_gram.append((line_list[i], line_list[i+1]))
    if two_gram[0][0]:
        final = init(two_gram[0][0], word_set=word_set)
    else:
        return []
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
        elif final[-1][0] == one_word_list[0]:
            continue
        else:
            one_word_list[1] = 'A'
            final.append(one_word_list)
    return final


def extract_2014():
    _data_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014/')))
    _write_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('2014_extract/')))
    dir_file = os.listdir(_data_path)
    log_f = log.logger('exclude', 'exclude_file.log')

    for dir in dir_file:
        # write_file_path = os.path.normpath(os.path.join(_write_path, os.path.dirname(dir+'/')))
        dir_file_path = os.path.normpath(os.path.join(_data_path, os.path.dirname(dir+'/')))
        file_name_list = os.listdir(dir_file_path)
        for file in file_name_list:
            file_path = os.path.join(dir_file_path, file)
            write_path = os.path.join(_write_path, file)
            with open(file_path) as f:
                file_name = os.path.basename(file_path)
                print file_name
                ff = open(write_path, 'w+')
                try:
                    for line in f:
                        if line.strip():
                            w_write_list = ex_role(line.strip().decode('utf-8'))
                            try:
                                write_line = ' '.join(i[0] + '/' + i[1] for i in w_write_list) + '\n'
                            except:
                                print w_write_list
                                exit()
                            ff.write(write_line.encode('utf-8'))
                except Exception, e:
                    log_f.filehand()
                    mes = str(file_name) + str(e)
                    log_f.f_waring(mes)
                ff.close()

if __name__ == '__main__':
    extract_2014()