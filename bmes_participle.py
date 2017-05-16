#-*-coding:utf-8
import os
import sys

def load_model(file_name):
    _model_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname('train/'+file_name)))
    fil = file(_model_path, 'rb')
    return eval(fil.read())

# start_prob = load_model('prob_start.py/')
# trans_prob = load_model('prob_trans.py/')
# emit_prob = load_model('prob_emit.py/')

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
    obs = obs.decode('utf8')
    for y in states:
        V[0][y] = start_p[y] * emis_p[y].get(obs[0], 0.0)
        path[y] = [y]

    for d in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max([(V[d-1][y0] * tran_p[y0].get(y, 0.0) * emis_p[y].get(obs[d], 0.0), y0) for y0 in states])
            V[d][y] = prob
            newpath[y] = path[state] + [y]

        path = newpath
    print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def cut_sentence(sentence):
    states = ['B', 'M', 'E', 'S']
    prob, prob_path = viterbi(sentence, states, start_prob, trans_prob, emit_prob)
    return prob, prob_path

if __name__ == '__main__':
    # test_str = '陆承宗淡漠的脸上眉头微蹙'
    test_str = '姚晨和老凌离婚了'
    prob, prob_path = cut_sentence(test_str)
    print prob
    print test_str
    print prob_path
    # print zip(test_str.decode('utf-8'), prob_path)