#-*-coding:utf-8
import os
import sys

def load_model(file_name):
    _model_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('train/'+file_name)))
    fil = file(_model_path, 'rb')
    print file
    return eval(fil.read())

start_prob = load_model('start_prob.py/')
trans_prob = load_model('trans_prob.py/')
emit_prob = load_model('emit_prob.py/')

def print_dptable(V):
    print '      ',
    for i in range(len(V)): print '%.7d' % i,
    print

    for y in V[0].keys():
        print '%.5s:' % y,
        for t in range(len(V)):
            print '%.7s' % ('%f' % V[t][y]),
        print

def viterbi(obs, states, start_p, tran_p, emis_p):
    V = [{}]
    path = {}

    for y in states:
        try:
            V[0][y] = start_p[y] * emis_p[y][obs[0]]
        except:
            print obs[0]
            exit()
        path[y] = [y]

    for d in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max([(V[d-1][y0] * tran_p[y0][y] * emis_p[y][obs[d]], y0) for y0 in states])
            V[d][y] = prob
            newpath[y] = path[y] + [y]

        path = newpath
    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def cut_sentence(sentence):
    global start_prob
    global trans_prob
    global emit_prob
    states = ['B', 'M', 'E', 'S']
    prob, prob_path = viterbi(sentence, states, start_prob, trans_prob, emit_prob)
    return prob, prob_path

if __name__ == '__main__':
    test_str = '江太玄没有丝毫犹豫，直接将几株药材拔了，然后挖坑，把武松埋了进去。'
    prob, prob_path = cut_sentence(test_str)
    print prob
    print test_str
    print prob_path